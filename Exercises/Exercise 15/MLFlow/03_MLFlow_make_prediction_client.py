import requests

# Define URLs for initialization and prediction
initialize_url = "http://127.0.0.1:5001/initialize"
predict_url = "http://127.0.0.1:5001/predict"

# Step 1: Initialize the model on the server
def initialize_model():
    try:
        response = requests.get(initialize_url)
        if response.status_code == 200:
            print("Initialization successful:", response.json())
        else:
            print("Initialization failed:", response.json())
            return False
    except Exception as e:
        print(f"Error during initialization: {e}")
        return False
    return True

# Step 2: Send prediction request to the server
def make_prediction(input_data):
    try:
        payload = {"inputs": input_data}
        response = requests.post(predict_url, json=payload)
        if response.status_code == 200:
            print("Prediction successful:", response.json())
        else:
            print("Prediction failed:", response.json())
    except Exception as e:
        print(f"Error during prediction: {e}")

if __name__ == "__main__":
    # Input data for prediction (update as per your model requirements)
    input_data = [
        [0.0, 0.0, 7.0, 14.0, 10.0, 0.0, 0.0, 0.0, 0.0, 7.0, 15.0, 4.0, 9.0, 11.0, 0.0, 0.0, 0.0, 9.0, 13.0, 0.0, 7.0, 16.0, 0.0, 0.0, 0.0, 3.0, 15.0, 16.0, 16.0, 16.0, 3.0, 0.0, 0.0, 0.0, 0.0, 4.0, 4.0, 12.0, 8.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.0, 12.0, 0.0, 0.0, 0.0, 11.0, 5.0, 0.0, 7.0, 13.0, 0.0, 0.0, 0.0, 5.0, 13.0, 16.0, 14.0, 6.0, 0.0],
        [0.0, 1.0, 10.0, 13.0, 2.0, 0.0, 0.0, 0.0, 0.0, 10.0, 16.0, 16.0, 12.0, 0.0, 0.0, 0.0, 0.0, 9.0, 9.0, 8.0, 16.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.0, 16.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0, 11.0, 15.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.0, 16.0, 13.0, 2.0, 0.0, 0.0, 0.0, 0.0, 14.0, 16.0, 16.0, 16.0, 13.0, 0.0, 0.0, 0.0, 9.0, 13.0, 11.0, 10.0, 9.0, 0.0],
        [0.0, 0.0, 0.0, 7.0, 12.0, 13.0, 1.0, 0.0, 0.0, 0.0, 8.0, 11.0, 1.0, 10.0, 8.0, 0.0, 0.0, 0.0, 12.0, 2.0, 1.0, 11.0, 7.0, 0.0, 0.0, 0.0, 10.0, 10.0, 14.0, 8.0, 0.0, 0.0, 0.0, 1.0, 7.0, 16.0, 9.0, 0.0, 0.0, 0.0, 0.0, 7.0, 16.0, 7.0, 14.0, 3.0, 0.0, 0.0, 0.0, 0.0, 7.0, 13.0, 5.0, 14.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.0, 15.0, 14.0, 2.0, 0.0],
        [0.0, 0.0, 4.0, 12.0, 16.0, 16.0, 11.0, 2.0, 0.0, 0.0, 15.0, 13.0, 8.0, 11.0, 8.0, 1.0, 0.0, 2.0, 15.0, 13.0, 16.0, 8.0, 0.0, 0.0, 0.0, 6.0, 16.0, 13.0, 13.0, 16.0, 2.0, 0.0, 0.0, 7.0, 11.0, 2.0, 2.0, 16.0, 6.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5.0, 15.0, 2.0, 0.0, 0.0, 0.0, 9.0, 6.0, 13.0, 10.0, 0.0, 0.0, 0.0, 0.0, 7.0, 14.0, 13.0, 1.0, 0.0, 0.0]
    ]

    # Initialize the model
    if initialize_model():
        # Make prediction if initialization succeeds
        make_prediction(input_data)
