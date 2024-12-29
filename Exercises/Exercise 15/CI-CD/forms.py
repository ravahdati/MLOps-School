from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField
from wtforms.validators import DataRequired

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
