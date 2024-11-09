from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo

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

class DiabetesPredictionForm(FlaskForm):
    age = FloatField('Age', validators=[DataRequired()])
    sex = FloatField('Sex', validators=[DataRequired()])
    bmi = FloatField('BMI', validators=[DataRequired()])
    bp = FloatField('Blood Pressure', validators=[DataRequired()])
    s1 = FloatField('S1 (Cholesterol)', validators=[DataRequired()])
    s2 = FloatField('S2 (Low-density lipoprotein)', validators=[DataRequired()])
    s3 = FloatField('S3 (High-density lipoprotein)', validators=[DataRequired()])
    s4 = FloatField('S4 (Triglycerides)', validators=[DataRequired()])
    s5 = FloatField('S5 (Blood Sugar)', validators=[DataRequired()])
    s6 = FloatField('S6 (Other Measurement)', validators=[DataRequired()])

    submit = SubmitField('Predict')
