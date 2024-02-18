import socket,os
from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify, Response
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from datetime import datetime
from MySQLdb import IntegrityError
from fpdf import FPDF
import random
import string
from db_config import MYSQL_CONFIG

app = Flask(__name__)

# Configure MySQL using imported settings
app.config['MYSQL_HOST'] = MYSQL_CONFIG['host']
app.config['MYSQL_USER'] = MYSQL_CONFIG['user']
app.config['MYSQL_PASSWORD'] = MYSQL_CONFIG['password']
app.config['MYSQL_DB'] = MYSQL_CONFIG['db']
app.config['MYSQL_CHARSET'] = MYSQL_CONFIG['charset']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = 'your_secret_key'  # Set a secret key for session management

mysql = MySQL(app)

# Determine the local Wi-Fi IP address dynamically
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# Routes
@app.route('/')
def home():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return render_template('home.html', error=session.pop('error', None), message=session.pop('message', None))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user and sha256_crypt.verify(password, user['password']):
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
        
    else:
        session['error'] = 'Invalid credentials'
        
    return redirect(url_for('home'))

@app.route('/signup', methods=['POST'])
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

    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        mysql.connection.commit()
        cur.close()

        session['message'] = 'Signup successful, please login'
        return redirect(url_for('home'))
    except IntegrityError:
        session['error'] = 'Email is already in use'
        return redirect(url_for('home'))

@app.route('/forgot-password', methods=['POST'])
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

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('home'))
    cur = mysql.connection.cursor()
    # Execute SQL query to count the number of rows in the production_info table
    cur.execute("SELECT COUNT(*) FROM production_info")
    result = cur.fetchone()

    # Close the cursor
    cur.close()

    # Extract the count from the result dictionary
    num_productions = result['COUNT(*)']

    return render_template('dashboard.html', num_productions=num_productions)

@app.route('/sales_order_form', methods=['GET'])
def form():
    return render_template('sales_order_form.html')

@app.route('/submit_sales_order', methods=['POST'])
def submit_sales_order():
    # Check if the user is logged in (just a placeholder, you should implement proper login mechanism)
    if 'logged_in' not in session:
        return redirect(url_for('home'))  # Assuming 'home' is the route for the home page

    # Get form data with proper error handling
    try:
        customer_name = request.form['customer_name']
        product_name = request.form['product_name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        order_date = request.form['order_date']
    except KeyError:
        flash('Error: Invalid form data received.', 'danger')
        return redirect(url_for('form'))

    # Here you would perform database operations, like inserting the data into your database
    # This part is left as an exercise; you need to add code to interact with your database

    # Set success or error flash message (just a placeholder, replace with your logic)
    # Assuming some_condition is the condition to determine success or failure
    if customer_name and product_name and quantity and price and order_date:
        flash('Sales order submitted successfully!', 'success')
    else:
        flash('Error occurred while submitting sales order.', 'danger')
    # Redirect to the sales order form page
    return redirect(url_for('form'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/report_form')
def report_form():
    return render_template('production_report.html')

@app.route('/generate_report', methods=['POST', 'GET'])
def generate_report():
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
    else:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM production_info WHERE date BETWEEN %s AND %s", (start_date, end_date))
    production_info = cur.fetchall()
    cur.close()

    return render_template('production_report.html', data=production_info, start_date=start_date, end_date=end_date)

@app.route('/export_csv', methods=['POST'])
def export_csv():
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM production_info WHERE date BETWEEN %s AND %s", (start_date, end_date))
    production_info = cur.fetchall()
    cur.close()

    output = ','.join(production_info[0].keys()) + '\n'
    for row in production_info:
        output += ','.join(map(str, row.values())) + '\n'

    return Response(output, mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=production_report.csv'})

@app.route('/export_pdf', methods=['POST'])
def export_pdf():
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM production_info WHERE date BETWEEN %s AND %s", (start_date, end_date))
    production_info = cur.fetchall()
    cur.close()

    for key in production_info[0].keys():
        pdf.cell(40, 10, key, ln=True)

    for row in production_info:
        for value in row.values():
            pdf.cell(40, 10, str(value), ln=True)

    pdf_output_path = "production_report.pdf"
    pdf.output(pdf_output_path)

    with open(pdf_output_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()

    os.remove(pdf_output_path)  # Delete the temporary PDF file

    return Response(pdf_data, mimetype='application/pdf', headers={'Content-Disposition': 'attachment; filename=production_report.pdf'})

@app.route('/production_form', methods=['GET', 'POST'])
def production_form():
    if request.method == 'POST':
        # Get form data
        date = request.form['date']
        order_number = request.form['order_number']
        product_type = request.form['product_type']
        quantity = request.form['quantity']
        quantity_unit = request.form['quantity_unit']
        machine = request.form['machine']
        shift = request.form['shift']

        # Insert form data into the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO production_info (date, order_number, product_type, quantity, quantity_unit, machine, shift) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (date, order_number, product_type, quantity, quantity_unit, machine, shift))
        mysql.connection.commit()
        cur.close()

        # Set success message
        session['message'] = 'Production information submitted successfully!'
        return redirect(url_for('dashboard'))

    return render_template('production_form.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host=local_ip)
