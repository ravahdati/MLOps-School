from flask import Flask, render_template, request, redirect, url_for, flash
from forms import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

@app.route('/', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        # If form validation passes, redirect to the same page
        return redirect(url_for('registration'))
    else:
        # Print form errors to the console
        print(form.errors)
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
