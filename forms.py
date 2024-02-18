from flask import Blueprint, render_template, request, jsonify, session
from flask_mysqldb import MySQL
from db_config import MYSQL_CONFIG

forms_app = Blueprint('forms', __name__)
mysql = MySQL()

@forms_app.route('/production_form')
def form():
    return render_template('production_form.html')

@forms_app.route('/submit_production', methods=['POST'])
def submit_production():
    # Check if the user is logged in
    if 'logged_in' not in session:
        return jsonify({"success": False, "message": "Not logged in"})

    # Get form data
    order_number = request.form['order_number']
    product_type = request.form['product_type']
    quantity = request.form['quantity']
    machine = request.form['machine']
    shift = request.form['shift']

    # Create cursor
    cur = mysql.connection.cursor()

    try:
        # Execute query to insert data into the database
        cur.execute("INSERT INTO production_info (order_number, product_type, quantity, machine, shift) VALUES (%s, %s, %s, %s, %s)", (order_number, product_type, quantity, machine, shift))

        # Commit to database
        mysql.connection.commit()

        # Close cursor
        cur.close()

        # Set success message
        message = "Form submitted successfully!"

        # Redirect to dashboard upon successful form submission
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
