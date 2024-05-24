from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management and CSRF protection

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username=? AND password=?"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        if user:
            return "Logged in successfully"
        else:
            return "Invalid credentials"
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production
