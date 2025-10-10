from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import requests
import firebase_admin
from firebase_admin import credentials, auth, firestore
import datetime

# --- Firebase Admin SDK Initialization ---
# This uses the secret key file you downloaded to give your backend access to your Firebase project.
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase Admin SDK initialized successfully.")
except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {e}")

app = Flask(__name__)
CORS(app)

# --- Model Loading ---
# Loads the trained machine learning model from the .pkl file when the server starts.
try:
    with open('crop_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    print("Crop recommendation model loaded successfully.")
except Exception as e:
    print(f"Error loading crop model: {e}")
    model = None

# --- Reusable function to get weather data ---
def get_weather(city_name, api_key):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        weather_data = response.json()
        
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        # Using a placeholder for rainfall as the free tier doesn't provide it reliably.
        rainfall = 100.0 
        print(f"Weather for {city_name}: Temp={temperature}, Humidity={humidity}")
        return temperature, humidity, rainfall
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        if response.status_code == 404:
            return "City not found", None, None
        return "Error", None, None
    except Exception as e:
        print(f"An error occurred fetching weather: {e}")
        return "Error", None, None

# --- Main API Endpoint ---
@app.route('/recommend', methods=['POST'])
def recommend():
    # Step 1: Verify the user is logged in
    try:
        id_token = request.headers.get('Authorization').split('Bearer ')[1]
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        print(f"Verified request from user UID: {uid}")
    except Exception as e:
        print(f"User verification failed: {e}")
        # If the token is invalid or missing, deny access.
        return jsonify({'error': 'Unauthorized. Please log in.'}), 401

    if model is None:
        return jsonify({'error': 'Model is not loaded, please check server logs.'}), 500

    try:
        # Step 2: Get data from the frontend
        data = request.get_json()
        print("Received data from frontend:", data)
        
        # Step 3: Fetch live weather data
        # IMPORTANT: Replace with your actual OpenWeatherMap API key
        api_key = "f6089cd84a151189ea32e8e582ba2720"
        city = data['city']
        temperature, humidity, rainfall = get_weather(city, api_key)

        if temperature == "City not found":
            return jsonify({'error': f'Could not find weather for "{city}". Please check spelling.'}), 404
        if temperature == "Error":
            return jsonify({'error': 'Failed to fetch weather data from the API.'}), 500

        # Step 4: Make a prediction with the AI model
        feature_list = [
            float(data['N']),
            float(data['P']),
            float(data['K']),
            temperature,
            humidity,
            float(data['ph']),
            rainfall
        ]
        features = np.array(feature_list).reshape(1, -1)
        prediction = model.predict(features)
        crop_result = prediction[0]
        print("Prediction successful:", crop_result)

        # Step 5: Save the result to the Firestore database
        user_recommendations_ref = db.collection('users').document(uid).collection('recommendations')
        user_recommendations_ref.add({
            'crop': crop_result,
            'inputs': data,
            'timestamp': datetime.datetime.now(datetime.timezone.utc)
        })
        print(f"Recommendation for user {uid} saved to Firestore.")

        # Step 6: Send the result back to the frontend
        return jsonify({'crop': crop_result})

    except Exception as e:
        print(f"An error occurred during the recommendation process: {e}")
        return jsonify({'error': 'An internal error occurred. Failed to process request.'}), 500

    # --- NEW ENDPOINT: To fetch user's recommendation history ---
@app.route('/history', methods=['GET'])
def get_history():
    # Step 1: Verify the user is logged in (same as before)
    try:
        id_token = request.headers.get('Authorization').split('Bearer ')[1]
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        print(f"Fetching history for user UID: {uid}")
    except Exception as e:
        print(f"User verification failed for history fetch: {e}")
        return jsonify({'error': 'Unauthorized. Please log in.'}), 401

    try:
        # Step 2: Query the Firestore database
        # Get a reference to the user's 'recommendations' sub-collection
        docs_ref = db.collection('users').document(uid).collection('recommendations')

        # Order the results by timestamp, with the most recent first
        docs = docs_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).stream()

        # Step 3: Format the data to send back to the frontend
        history = []
        for doc in docs:
            data = doc.to_dict()
            # Make the timestamp human-readable
            data['timestamp'] = data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            history.append(data)

        print(f"Found {len(history)} records for user {uid}.")
        return jsonify(history)

    except Exception as e:
        print(f"Error fetching history: {e}")
        return jsonify({'error': 'Failed to fetch recommendation history.'}), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)
