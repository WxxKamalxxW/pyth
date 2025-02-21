from datetime import timedelta

from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_session import Session
from functools import wraps

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'kamal'
app.config['MYSQL_DB'] = 'login'

# Session configuration
app.config['SECRET_KEY'] = 'kamal'  # Used for encrypting session data
app.config['SESSION_TYPE'] = 'filesystem'  # Store session data on the server
app.config['SESSION_PERMANENT'] = False  # Session will end when the browser closes
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Auto logout after 30 minutes


mysql = MySQL(app)
Session(app)

# Helper function to restrict access to logged-in users
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('home'))  # Redirect to login page if not logged in
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('login.html')  # Ensure this file exists in the templates folder

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, role FROM users WHERE email = %s AND password = %s", (email, password))
    user = cur.fetchone()
    cur.close()

    if user:
        session['user_id'] = user[0]  # Store user ID in session
        session['role'] = user[1]  # Store user role in session

        return jsonify({"status": "success", "role": user[1], "message": "Login successful!"}), 200
    else:
        return jsonify({"message": "Invalid credentials!"}), 401

@app.route('/dashboard')
@login_required  # Protect the dashboard route
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()  # Clear session data
    return redirect(url_for('home'))  # Redirect to login page

if __name__ == '__main__':
    app.run(debug=True)
