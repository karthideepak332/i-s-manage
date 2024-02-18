from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
import random
import string

auth_app = Blueprint('auth', __name__)

mysql = MySQL()

@auth_app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user and sha256_crypt.verify(password, user[2]):
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    else:
        session['error'] = 'Invalid credentials'
        return redirect(url_for('home'))

@auth_app.route('/signup', methods=['POST'])
def signup():
    name = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    # Validate inputs
    if not (name and email and password and confirm_password):
        session['error'] = 'All fields are required'
        return redirect(url_for('home'))

    if password != confirm_password:
        session['error'] = 'Passwords do not match'
        return redirect(url_for('home'))

    hashed_password = sha256_crypt.encrypt(password)

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO user (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
    mysql.connection.commit()
    cur.close()

    session['message'] = 'Signup successful, please login'
    return redirect(url_for('home'))

@auth_app.route('/forgot-password', methods=['POST'])
def forgot_password():
    email = request.form.get('email')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user:
        # Generate a unique token for password reset
        token = generate_reset_token()

        # Store the token in the database
        cur = mysql.connection.cursor()
        cur.execute("UPDATE user SET reset_token = %s WHERE email = %s", (token, email))
        mysql.connection.commit()
        cur.close()

        # Send email to the user with the token (This part is not implemented in this example)
        print(f"Password reset token for email {email}: {token}")
        return jsonify({"message": "Password reset instructions sent to your email!"}), 200
    else:
        return jsonify({"error": "Email address not found"}), 404

def generate_reset_token():
    # Generate a random token (8 characters long)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))
