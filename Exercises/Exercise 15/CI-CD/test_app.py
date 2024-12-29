import pytest
from flask import Flask, jsonify
from app import app  # Import your Flask app from the provided code

@pytest.fixture
def client():
    """Fixture to set up a test client."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'  # Use a different secret key for testing
    with app.test_client() as client:
        yield client

def test_prediction_valid(client, monkeypatch):
    """Test the /prediction route with valid data."""
    # Mock the predict_diabetes function
    def mock_predict_diabetes(input_data):
        return [1]  # Mocked prediction (High progression)

    # Use monkeypatch to replace the real function with the mock
    monkeypatch.setattr('model.predict_diabetes', mock_predict_diabetes)

    # Prepare valid input data
    data = {
        "features": [50, 1, 25.0, 80.0, 100.0, 150.0, 200.0, 250.0, 300.0, 350.0]
    }

    response = client.post('/prediction', json=data)
    assert response.status_code == 200
    assert response.get_json() == {"prediction": 1}

def test_prediction_invalid(client):
    """Test the /prediction route with invalid data."""
    # Prepare invalid input data
    data = {"invalid_key": [1, 2, 3]}

    response = client.post('/prediction', json=data)
    assert response.status_code == 400
    assert "error" in response.get_json()