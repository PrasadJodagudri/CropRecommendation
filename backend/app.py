from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np # Import numpy

# Create the Flask application
app = Flask(__name__)
CORS(app)

# --- Model Loading ---
# Load the trained machine learning model from the .pkl file
# This happens only ONCE when the server starts.
try:
    with open('crop_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# --- API Endpoint ---
# Defines the '/recommend' endpoint
@app.route('/recommend', methods=['POST'])
def recommend():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        # Get the JSON data sent from the frontend
        data = request.get_json()
        print("Received data:", data)

        # CRITICAL: Create the feature list in the EXACT order the model expects
        # Based on the dataset: N, P, K, temperature, humidity, ph, rainfall
        feature_list = [
            float(data['N']),
            float(data['P']),
            float(data['K']),
            float(data['temperature']),
            float(data['humidity']),
            float(data['ph']),
            float(data['rainfall'])
        ]

        # Convert the list to a 2D NumPy array for the model
        features = np.array(feature_list).reshape(1, -1)

        # Make a prediction
        prediction = model.predict(features)
        crop_result = prediction[0] # The result is an array, so we take the first element

        print("Prediction successful:", crop_result)
        # Return the prediction in a JSON response
        return jsonify({'crop': crop_result})

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': 'Failed to make prediction'}), 500

# --- Run the App ---
if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)