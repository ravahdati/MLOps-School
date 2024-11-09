from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from model import predict_diabetes
from forms import RegistrationForm, LoginForm, DiabetesPredictionForm
import numpy as np


app = Flask(__name__)

#app configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project2.db'
app.config['SECRET_KEY'] = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # User info data
    fullname = db.Column(db.String(300), nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class PredictionResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prediction = db.Column(db.String(50), nullable=False)  # Store 'Low progression' or 'High progression'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Diabetes-related features
    age = db.Column(db.Float, nullable=False)
    sex = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    bp = db.Column(db.Float, nullable=False)
    s1 = db.Column(db.Float, nullable=False)
    s2 = db.Column(db.Float, nullable=False)
    s3 = db.Column(db.Float, nullable=False)
    s4 = db.Column(db.Float, nullable=False)
    s5 = db.Column(db.Float, nullable=False)
    s6 = db.Column(db.Float, nullable=False)

    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Automatically set timestamp


def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            flash('Please Login to continue!', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@app.route('/')
def home():
    return render_template('index.html', title='Home')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(fullname=fullname, username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration Successful, Please Login to Panel.', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['username'] = user.username

            flash('You’ve successfully logged in!', 'success')
            return redirect(url_for('input_data'))
        else:
            flash('Login failed, Check your username or password.', 'danger')

    return render_template('login.html', form=form, title = 'Login' )

@app.route('/input', methods=['GET', 'POST'])
@login_required
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

        # Make prediction using the loaded model
        prediction = predict_diabetes(input_data)

        # Interpret the result (1: High progression, 0: Low progression)
        prediction_label = "High progression" if prediction[0] == 1 else "Low progression"
        
        # Get the logged-in user from session
        user = User.query.filter_by(username=session['username']).first()

        # Save the result in the database
        prediction_result = PredictionResult(
            prediction=prediction_label,
            user_id=user.id,
            age=age,
            sex=sex,
            bmi=bmi,
            bp=bp,
            s1=s1,
            s2=s2,
            s3=s3,
            s4=s4,
            s5=s5,
            s6=s6
        )
        db.session.add(prediction_result)
        db.session.commit()

        # Display prediction result
        flash('The Prediction Result: ' + prediction_label , 'success')

        return redirect(url_for('result'))

    return render_template('input.html', form=form, title='Input Data')

@app.route('/result')
@login_required
def result():
    return render_template('result.html', title='Result')

@app.route('/history', defaults={'prediction_id': None})
@app.route('/history/<int:prediction_id>')
@login_required
def history(prediction_id):
    user = User.query.filter_by(username=session['username']).first()
    if prediction_id is None:
        # If no prediction_id is provided, show the list of all predictions for the logged-in user
        predictions = PredictionResult.query.filter_by(user_id=user.id).order_by(PredictionResult.timestamp.desc()).all()
        return render_template('history.html', title='Prediction History', predictions=predictions)
    else:
        # If a prediction_id is provided, show the details for that specific prediction
        prediction = PredictionResult.query.filter_by(id=prediction_id, user_id=user.id).first_or_404()
        return render_template('history_details.html', title='Prediction Details', prediction=prediction)

@app.route('/logout')
def logout():
    session.pop('username')
    flash('You have been Logged out', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0',port=5000)
