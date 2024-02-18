from flask import Blueprint, render_template

# Define blueprints
about_bp = Blueprint('about', __name__)
contact_bp = Blueprint('contact', __name__)
dashboard_bp = Blueprint('dashboard', __name__)

# Routes for About
@about_bp.route('/about')
def about():
    # Function implementation as before
    return render_template('about.html')

# Routes for Contact
@contact_bp.route('/contact')
def contact():
    return render_template('contact.html')

# Routes for Dashboard
@dashboard_bp.route('/dashboard')
def dashboard():
    # Function implementation as before
    return render_template('dashboard.html')
