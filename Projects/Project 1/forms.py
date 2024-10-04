from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from sklearn.datasets import load_breast_cancer

class RegistrationForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired(), Length(min=10, message="Fullname must be at least 10 characters long.")])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, message="Username must be at least 3 characters long.")])
    email = EmailField('Email', validators=[DataRequired(), Email(message="Please enter a valid email.")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message="Password must be at least 8 characters long.")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match.")])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, message="Username must be at least 3 characters long.")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message="Password must be at least 8 characters long.")])
    submit = SubmitField('Login')

class PredictionForm(FlaskForm):
    # Mean features
    mean_radius = FloatField('Mean Radius', validators=[DataRequired()])
    mean_texture = FloatField('Mean Texture', validators=[DataRequired()])
    mean_perimeter = FloatField('Mean Perimeter', validators=[DataRequired()])
    mean_area = FloatField('Mean Area', validators=[DataRequired()])
    mean_smoothness = FloatField('Mean Smoothness', validators=[DataRequired()])
    mean_compactness = FloatField('Mean Compactness', validators=[DataRequired()])
    mean_concavity = FloatField('Mean Concavity', validators=[DataRequired()])
    mean_concave_points = FloatField('Mean Concave Points', validators=[DataRequired()])
    mean_symmetry = FloatField('Mean Symmetry', validators=[DataRequired()])
    mean_fractal_dimension = FloatField('Mean Fractal Dimension', validators=[DataRequired()])

    # Error features
    radius_error = FloatField('Radius Error', validators=[DataRequired()])
    texture_error = FloatField('Texture Error', validators=[DataRequired()])
    perimeter_error = FloatField('Perimeter Error', validators=[DataRequired()])
    area_error = FloatField('Area Error', validators=[DataRequired()])
    smoothness_error = FloatField('Smoothness Error', validators=[DataRequired()])
    compactness_error = FloatField('Compactness Error', validators=[DataRequired()])
    concavity_error = FloatField('Concavity Error', validators=[DataRequired()])
    concave_points_error = FloatField('Concave Points Error', validators=[DataRequired()])
    symmetry_error = FloatField('Symmetry Error', validators=[DataRequired()])
    fractal_dimension_error = FloatField('Fractal Dimension Error', validators=[DataRequired()])

    # Worst features
    worst_radius = FloatField('Worst Radius', validators=[DataRequired()])
    worst_texture = FloatField('Worst Texture', validators=[DataRequired()])
    worst_perimeter = FloatField('Worst Perimeter', validators=[DataRequired()])
    worst_area = FloatField('Worst Area', validators=[DataRequired()])
    worst_smoothness = FloatField('Worst Smoothness', validators=[DataRequired()])
    worst_compactness = FloatField('Worst Compactness', validators=[DataRequired()])
    worst_concavity = FloatField('Worst Concavity', validators=[DataRequired()])
    worst_concave_points = FloatField('Worst Concave Points', validators=[DataRequired()])
    worst_symmetry = FloatField('Worst Symmetry', validators=[DataRequired()])
    worst_fractal_dimension = FloatField('Worst Fractal Dimension', validators=[DataRequired()])

    # Submit button
    submit = SubmitField('Predict')
