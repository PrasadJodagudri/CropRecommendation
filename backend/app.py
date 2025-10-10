from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import requests # Make sure to import requests

app = Flask(__name__)
CORS(app)

# --- Model Loading ---
try:
    with open('crop_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# --- NEW FUNCTION: To get weather data ---
def get_weather(city_name, api_key):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    try:
        response = requests.get(api_url)
        response.raise_for_status() # Raises an error for bad responses (4xx or 5xx)
        weather_data = response.json()

        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        # Using a placeholder for rainfall as the free tier doesn't provide it reliably.
        # This is a reasonable approximation for many regions during growing seasons.
        rainfall = 100.0
        print(f"Weather for {city_name}: Temp={temperature}, Humidity={humidity}")
        return temperature, humidity, rainfall
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        # Check if the error is a 404 (city not found)
        if response.status_code == 404:
            return "City not found", None, None
        return "Error", None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error", None, None

# --- UPDATED: API Endpoint ---
@app.route('/recommend', methods=['POST'])
def recommend():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.get_json()
        print("Received data from frontend:", data)

        # --- API Key and City ---
        # IMPORTANT: Replace with your actual API key
        api_key = "f6089cd84a151189ea32e8e582ba2720" 
        city = data['city']

        temperature, humidity, rainfall = get_weather(city, api_key)

        if temperature == "City not found":
             return jsonify({'error': f'Could not find weather data for "{city}". Please check the spelling.'}), 404
        if temperature == "Error":
             return jsonify({'error': 'Failed to fetch weather data. The API might be down.'}), 500

        # --- Build Feature List with Live Data ---
        feature_list = [
            float(data['N']),
            float(data['P']),
            float(data['K']),
            temperature, # From API
            humidity,    # From API
            float(data['ph']),
            rainfall     # Using our placeholder value
        ]

        features = np.array(feature_list).reshape(1, -1)
        prediction = model.predict(features)
        crop_result = prediction[0]

        print("Prediction successful:", crop_result)
        return jsonify({'crop': crop_result})

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': 'Failed to make prediction'}), 500

# --- Run the App ---
if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)