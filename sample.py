@app.route('/production_form')
def form():
    return render_template('production_form.html')

@app.route('/submit_production', methods=['POST'])
def submit_production():
    # Check if the user is logged in
    if 'logged_in' not in session:
        return redirect(url_for('home'))

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