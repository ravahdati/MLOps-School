import pickle

with open('cancer_model.pkl', 'rb') as f :
    model = pickle.load(f)

def predict_price(features):
    predictions = model.predict([features])
    return predictions[0]