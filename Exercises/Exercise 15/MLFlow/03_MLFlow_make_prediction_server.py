import mlflow
import mlflow.pyfunc
from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

# Global variable for the model
model = None

# Set MLflow tracking URI
mlflow.set_tracking_uri("http://127.0.0.1:5000")

# Load the Production model when the server starts
@app.route('/initialize', methods=['GET'])
def initialize():
    global model
    try:
        # Correct the model URI to point to the MLflow model registry
        model_uri = "models:/digits_random_forest_classifier/1"  # Ensure this matches your registered model
        model = mlflow.pyfunc.load_model(model_uri)
        return jsonify({"status": "Model loaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define prediction route
@app.route('/predict', methods=['POST'])
def predict():
    global model
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        # Extract input data from the request
        input_data = request.json.get("inputs", None)
        if input_data is None:
            return jsonify({"error": "No input data provided"}), 400

        # Convert input to a NumPy array
        input_array = np.array(input_data)

        # Reshape if the input is a single sample
        if len(input_array.shape) == 1:
            input_array = input_array.reshape(1, -1)

        # Predict using the model
        predictions = model.predict(input_array)
        return jsonify({"predictions": predictions.tolist()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
