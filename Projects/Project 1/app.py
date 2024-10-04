from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from model import predict_breast_cancer
from forms import RegistrationForm, LoginForm, PredictionForm


app = Flask(__name__)

#app configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project1.db'
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
    prediction = db.Column(db.String(50), nullable=False)  # Store 'Benign' or 'Malignant'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Mean feature columns
    mean_radius = db.Column(db.Float, nullable=False)
    mean_texture = db.Column(db.Float, nullable=False)
    mean_perimeter = db.Column(db.Float, nullable=False)
    mean_area = db.Column(db.Float, nullable=False)
    mean_smoothness = db.Column(db.Float, nullable=False)
    mean_compactness = db.Column(db.Float, nullable=False)
    mean_concavity = db.Column(db.Float, nullable=False)
    mean_concave_points = db.Column(db.Float, nullable=False)
    mean_symmetry = db.Column(db.Float, nullable=False)
    mean_fractal_dimension = db.Column(db.Float, nullable=False)

    # Error feature columns
    radius_error = db.Column(db.Float, nullable=False)
    texture_error = db.Column(db.Float, nullable=False)
    perimeter_error = db.Column(db.Float, nullable=False)
    area_error = db.Column(db.Float, nullable=False)
    smoothness_error = db.Column(db.Float, nullable=False)
    compactness_error = db.Column(db.Float, nullable=False)
    concavity_error = db.Column(db.Float, nullable=False)
    concave_points_error = db.Column(db.Float, nullable=False)
    symmetry_error = db.Column(db.Float, nullable=False)
    fractal_dimension_error = db.Column(db.Float, nullable=False)

    # Worst feature columns
    worst_radius = db.Column(db.Float, nullable=False)
    worst_texture = db.Column(db.Float, nullable=False)
    worst_perimeter = db.Column(db.Float, nullable=False)
    worst_area = db.Column(db.Float, nullable=False)
    worst_smoothness = db.Column(db.Float, nullable=False)
    worst_compactness = db.Column(db.Float, nullable=False)
    worst_concavity = db.Column(db.Float, nullable=False)
    worst_concave_points = db.Column(db.Float, nullable=False)
    worst_symmetry = db.Column(db.Float, nullable=False)
    worst_fractal_dimension = db.Column(db.Float, nullable=False)

    # Add timestamp column
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Automatically set to current time


def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to continue!', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@app.route('/')
def home():
    return render_template('index.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        print("Form is valid and POST request")
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(fullname=fullname, username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration Successful, Please Login to Panel.', 'success')

        return redirect(url_for('login'))
    else:
        print("Form did not validate or request was not POST")

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
    form = PredictionForm()  # Use the static form
    if form.validate_on_submit():
        # Collect input data from the form fields in the correct order
        input_data = [
            form.mean_radius.data, form.mean_texture.data, form.mean_perimeter.data, form.mean_area.data,
            form.mean_smoothness.data, form.mean_compactness.data, form.mean_concavity.data,
            form.mean_concave_points.data, form.mean_symmetry.data, form.mean_fractal_dimension.data,
            form.radius_error.data, form.texture_error.data, form.perimeter_error.data, form.area_error.data,
            form.smoothness_error.data, form.compactness_error.data, form.concavity_error.data,
            form.concave_points_error.data, form.symmetry_error.data, form.fractal_dimension_error.data,
            form.worst_radius.data, form.worst_texture.data, form.worst_perimeter.data, form.worst_area.data,
            form.worst_smoothness.data, form.worst_compactness.data, form.worst_concavity.data,
            form.worst_concave_points.data, form.worst_symmetry.data, form.worst_fractal_dimension.data
        ]

        # Perform prediction
        predict = predict_breast_cancer(input_data)

        # Determine the prediction result (Benign or Malignant)
        prediction_label = 'Benign' if predict == 0 else 'Malignant'

        # Get the logged-in user from session
        user = User.query.filter_by(username=session['username']).first()

        # Save the prediction result to the database
        prediction_result = PredictionResult(
            prediction=prediction_label,
            user_id=user.id,
            mean_radius=form.mean_radius.data,
            mean_texture=form.mean_texture.data,
            mean_perimeter=form.mean_perimeter.data,
            mean_area=form.mean_area.data,
            mean_smoothness=form.mean_smoothness.data,
            mean_compactness=form.mean_compactness.data,
            mean_concavity=form.mean_concavity.data,
            mean_concave_points=form.mean_concave_points.data,
            mean_symmetry=form.mean_symmetry.data,
            mean_fractal_dimension=form.mean_fractal_dimension.data,
            radius_error=form.radius_error.data,
            texture_error=form.texture_error.data,
            perimeter_error=form.perimeter_error.data,
            area_error=form.area_error.data,
            smoothness_error=form.smoothness_error.data,
            compactness_error=form.compactness_error.data,
            concavity_error=form.concavity_error.data,
            concave_points_error=form.concave_points_error.data,
            symmetry_error=form.symmetry_error.data,
            fractal_dimension_error=form.fractal_dimension_error.data,
            worst_radius=form.worst_radius.data,
            worst_texture=form.worst_texture.data,
            worst_perimeter=form.worst_perimeter.data,
            worst_area=form.worst_area.data,
            worst_smoothness=form.worst_smoothness.data,
            worst_compactness=form.worst_compactness.data,
            worst_concavity=form.worst_concavity.data,
            worst_concave_points=form.worst_concave_points.data,
            worst_symmetry=form.worst_symmetry.data,
            worst_fractal_dimension=form.worst_fractal_dimension.data
        )

        db.session.add(prediction_result)
        db.session.commit()

        # Display prediction result
        if predict == 0:
            flash('The Prediction Result: Benign', 'success')
        else:
            flash('The Prediction Result: Malignant', 'danger')

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
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
