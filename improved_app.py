from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for Flask-WTF CSRF protection

# Define the LoginForm using Flask-WTF
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
        conn.close()  # Close the database connection
        if user:
            return "Logged in successfully"  # Ideally redirect to a dashboard
        else:
            return "Invalid credentials"  # Can be enhanced with flash messages
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run()
