from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from model import predict_diabetes
from forms import DiabetesPredictionForm
import numpy as np # HRKU-76b796a6-df25-462d-8790-ebd8c194c5f5

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

@app.route('/')
def home():
    return render_template('index.html', title='Home')

@app.route('/input', methods=['GET', 'POST'])
def input_data():
    form = DiabetesPredictionForm()  # Use the static form
    if form.validate_on_submit():
        # Retrieve data using request.form[]
        age = float(request.form['age'])
        sex = float(request.form['sex'])
        bmi = float(request.form['bmi'])
        bp = float(request.form['bp'])
        s1 = float(request.form['s1'])
        s2 = float(request.form['s2'])
        s3 = float(request.form['s3'])
        s4 = float(request.form['s4'])
        s5 = float(request.form['s5'])
        s6 = float(request.form['s6'])

        # Prepare the input data for prediction
        input_data = np.array([age, sex, bmi, bp, s1, s2, s3, s4, s5, s6])

        # Make prediction using the /prediction route
        response = predict_diabetes(input_data)
        prediction_label = "High progression" if response[0] == 1 else "Low progression"

        # Display prediction result
        flash('The Prediction Result: ' + prediction_label , 'success')

        return redirect(url_for('result'))

    return render_template('input.html', form=form, title='Input Data')

@app.route('/prediction', methods=['POST'])
def prediction():
    try:
        # Parse JSON input
        data = request.get_json()
        input_data = np.array(data['features'])

        # Make prediction using the model
        prediction = predict_diabetes(input_data)

        # Return the prediction as JSON
        return jsonify({"prediction": int(prediction[0])})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/result')
def result():
    return render_template('result.html', title='Result')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)