# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1d5CbjeRCmZFBq7aNlwaK6RtmLQBAN2bL
"""

import joblib
import numpy as np

def load_model():
    # Load the trained model
    model = joblib.load('iris_model.joblib')
    return model

def get_user_input():
    # Get the four features from the user
    print("Please enter the following features:")
    sepal_length = float(input("Sepal length (cm): "))
    sepal_width = float(input("Sepal width (cm): "))
    petal_length = float(input("Petal length (cm): "))
    petal_width = float(input("Petal width (cm): "))
    return np.array([[sepal_length, sepal_width, petal_length, petal_width]])

def predict_iris_type(model, features):
    # Predict the type of iris
    prediction = model.predict(features)
    return prediction[0]

def main():
    model = load_model()
    features = get_user_input()
    iris_type = predict_iris_type(model, features)
    iris_names = ['setosa', 'versicolor', 'virginica']
    print(f"The predicted type of iris is: {iris_names[iris_type]}")

if __name__ == "__main__":
    main()