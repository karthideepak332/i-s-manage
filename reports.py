from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from db_config import MYSQL_CONFIG
from flask import Blueprint
reports_app = Blueprint('reports', __name__)

app = Flask(__name__)
mysql = MySQL(app)

# Routes
@app.route('/generate_report')
def generate_report():
    # Function implementation as before
     # Connect to the database
    cursor = mysql.connection.cursor()

    # Retrieve data from the database
    cursor.execute("SELECT * FROM production_info")
    data = cursor.fetchall()

    # Close database connection
    cursor.close()

    # Pass data to the template for rendering
    return render_template('production_report.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
