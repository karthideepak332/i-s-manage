from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from db_config import MYSQL_CONFIG
import random
import string


app = Flask(__name__)

# Configure MySQL using imported settings
app.config['MYSQL_HOST'] = MYSQL_CONFIG['host']
app.config['MYSQL_USER'] = MYSQL_CONFIG['user']
app.config['MYSQL_PASSWORD'] = MYSQL_CONFIG['password']
app.config['MYSQL_DB'] = MYSQL_CONFIG['db']
app.config['MYSQL_CHARSET'] = MYSQL_CONFIG['charset']
app.secret_key = 'your_secret_key'  # Set a secret key for session management

mysql = MySQL(app)

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

    if user and sha256_crypt.verify(password, user[2]):
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

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO user (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
    mysql.connection.commit()
    cur.close()

    session['message'] = 'Signup successful, please login'
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
        return redirect(url_for('dashboard'))
    cur = mysql.connection.cursor()
    # Execute SQL query to count the number of rows in the production_info table
    cur.execute("SELECT COUNT(*) FROM production_info")
    result = cur.fetchone()

    # Close the cursor
    cur.close()

    # Extract the count from the result tuple
    num_productions = result[0]

    return render_template('dashboard.html',num_productions=num_productions)
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route to generate report
@app.route('/generate_report')
def generate_report():
    # Connect to the database
    cursor = mysql.connection.cursor()

    # Retrieve data from the database
    cursor.execute("SELECT * FROM production_info")
    data = cursor.fetchall()

    # Close database connection
    cursor.close()

    # Pass data to the template for rendering
    return render_template('production_report.html', data=data)


('/')
def sales_order_form():
    return render_template('sales_order_form.html')

@app.route('/sales_order', methods=['POST,GET'])
def sales_order():
    if request.method == 'POST':
        # Get form data
        customer_name = request.form['customer_name']
        product_name = request.form['product_name']
        quantity = request.form['quantity']
        price = request.form['price']
        order_date = request.form['order_date']

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query to insert data into the sales_orders table
        cur.execute("INSERT INTO sales_orders (customer_name, product_name, quantity, price, order_date) VALUES (%s, %s, %s, %s, %s)",
                    (customer_name, product_name, quantity, price, order_date))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        return redirect(url_for('sales_order_form'))

@app.route('/sales_order_form')
def sales_order_form():
    return render_template('sales_order_form.html')

@app.route('/submit_sales_order', methods=['POST'])
def submit_sales_order():
    # Check if the user is logged in
    if 'logged_in' not in session:
        return redirect(url_for('home'))  # Assuming 'home' is the route for the home page

    # Get form data
    customer_name = request.form['customer_name']
    product_name = request.form['product_name']
    quantity = request.form['quantity']
    price = request.form['price']
    order_date = request.form['order_date']

    # Create cursor
    cur = mysql.connection.cursor()

    try:
        # Execute query to insert data into the database
        cur.execute("INSERT INTO sales_orders (customer_name, product_name, quantity, price, order_date) VALUES (%s, %s, %s, %s, %s)",
                    (customer_name, product_name, quantity, price, order_date))

        # Commit to database
        mysql.connection.commit()

        # Close cursor
        cur.close()

        # Set success message
        message = "Sales order submitted successfully!"

        # Return success message
        return jsonify({"success": True, "message": message})
    except Exception as e:
        # Rollback in case of error
        mysql.connection.rollback()

        # Close cursor
        cur.close()

        # Set error message
        message = f"Error occurred: {str(e)}"

        # Return error message
        return jsonify({"success": False, "message": message})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
