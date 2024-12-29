import pickle

with open('diabetes_logistic_model.pkl', 'rb') as f :
    model = pickle.load(f)

def predict_diabetes(features):
    predictions = model.predict([features])
    return predictions
