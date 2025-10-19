from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import requests
import firebase_admin
from firebase_admin import credentials, auth, firestore
import datetime
import json

# --- Initialization ---
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    print(f"Error initializing Firebase: {e}")

app = Flask(__name__)
CORS(app)

# --- Data and Model Loading ---
try:
    with open('crop_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('crop_npk_targets.json', 'r') as f:
        npk_targets = json.load(f)
    with open('crop_market_prices.json', 'r') as f:
        market_prices = json.load(f)
    print("All data and models loaded successfully.")
except Exception as e:
    print(f"Error loading data files: {e}")
    model, npk_targets, market_prices = None, {}, {}

# --- Helper Functions ---
def get_weather(city_name, api_key):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        weather_data = response.json()
        return weather_data['main']['temp'], weather_data['main']['humidity'], 100.0
    except Exception:
        return "Error", None, None

def calculate_fertilizer(user_soil, target_soil):
    fertilizer_suggestion = {}
    urea_N, dap_N, dap_P, mop_K = 0.46, 0.18, 0.46, 0.60
    n_deficit = max(0, target_soil.get('N', 0) - user_soil.get('N', 0))
    p_deficit = max(0, target_soil.get('P', 0) - user_soil.get('P', 0))
    k_deficit = max(0, target_soil.get('K', 0) - user_soil.get('K', 0))
    dap_needed = p_deficit / dap_P if dap_P > 0 else 0
    urea_needed = max(0, n_deficit - (dap_needed * dap_N)) / urea_N if urea_N > 0 else 0
    mop_needed = k_deficit / mop_K if mop_K > 0 else 0
    fertilizer_suggestion['urea'] = round(urea_needed, 2)
    fertilizer_suggestion['dap'] = round(dap_needed, 2)
    fertilizer_suggestion['mop'] = round(mop_needed, 2)
    return fertilizer_suggestion

# --- The "Super" Recommendation Endpoint ---
@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        id_token = request.headers.get('Authorization').split('Bearer ')[1]
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        
        data = request.get_json()
        user_soil = {'N': float(data.get('N', 0)), 'P': float(data.get('P', 0)), 'K': float(data.get('K', 0))}

        api_key = "f6089cd84a151189ea32e8e582ba2720"
        temperature, humidity, rainfall = get_weather(data['city'], api_key)
        if temperature == "Error": return jsonify({'error': 'Failed to fetch weather data.'}), 500
        
        feature_list = [user_soil['N'], user_soil['P'], user_soil['K'], temperature, humidity, float(data['ph']), rainfall]
        features = np.array(feature_list).reshape(1, -1)
        
        probabilities = model.predict_proba(features)[0]
        top_indices = np.argsort(probabilities)[-3:][::-1]
        
        recommendations = []
        for i in top_indices:
            crop_name = model.classes_[i]
            target_npk = npk_targets.get(crop_name.lower())
            recommendations.append({
                'crop': crop_name,
                'confidence': round(probabilities[i] * 100, 2),
                'market_price': market_prices.get(crop_name.lower(), "N/A"),
                'fertilizer_suggestion': calculate_fertilizer(user_soil, target_npk) if target_npk else None
            })
        
        top_crop_name = recommendations[0]['crop']
        
        crop_details = None
        try:
            info_response = requests.get(f'http://localhost:8080/api/crop-info/{top_crop_name}')
            if info_response.status_code == 200:
                crop_details = info_response.json()
        except requests.exceptions.RequestException as e:
            print(f"Could not connect to Java service: {e}")

        final_response = {
            'recommendations': recommendations,
            'details': crop_details
        }
        
        db.collection('users').document(uid).collection('recommendations').add({
            'crop': top_crop_name, 'inputs': data, 'timestamp': datetime.datetime.now(datetime.timezone.utc)
        })
        
        return jsonify(final_response)

    except Exception as e:
        print(f"An error occurred during recommendation: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500

# --- History Endpoint (No changes needed) ---
@app.route('/history', methods=['GET'])
def get_history():
    try:
        id_token = request.headers.get('Authorization').split('Bearer ')[1]
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        docs_ref = db.collection('users').document(uid).collection('recommendations')
        docs = docs_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
        history = []
        for doc in docs:
            data = doc.to_dict()
            if 'timestamp' in data and hasattr(data['timestamp'], 'strftime'):
                data['timestamp'] = data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            history.append(data)
        return jsonify(history)
    except Exception as e:
        print(f"Error fetching history: {e}")
        return jsonify({'error': 'Failed to fetch recommendation history.'}), 500

if __name__ == '__main__':
    app.run(debug=True)