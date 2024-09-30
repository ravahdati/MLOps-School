from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
#from model import predict_price
from forms import RegistrationForm, LoginForm


app = Flask(__name__)

#app configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(300), nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)


def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            flash('You need to login first!', 'danger')
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

@app.route('/predict')
@login_required
def predict():
    return render_template('predict.html')

@app.route('/result')
@login_required
def result():
    return render_template('result.html')

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

        flash('Registration successful, Please log in.', 'success')

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

            flash(' Login successful!', 'success')
            return redirect(url_for('input_data'))
        else:
            flash('Login failed, Check your username or password', 'danger')

    return render_template('login.html', form=form, title = 'Login' )


@app.route('/logout')
def logout():
    session.pop('username')
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
