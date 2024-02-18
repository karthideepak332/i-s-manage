import socket
from flask import Flask
from auth import auth_app
from forms import forms_app
from reports import reports_app
from page_routes import about_bp, contact_bp, dashboard_bp

app = Flask(__name__)

# Determine the local Wi-Fi IP address dynamically
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# Construct the base URL using the local IP address
base_url = f"http://{local_ip}:5000"  # Assuming Flask runs on port 5000

# Register blueprints
app.register_blueprint(auth_app, url_prefix="/auth")
app.register_blueprint(forms_app, url_prefix="/forms")
app.register_blueprint(reports_app, url_prefix="/reports")
app.register_blueprint(about_bp, url_prefix="/about")
app.register_blueprint(contact_bp, url_prefix="/contact")
app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

# Define a route for the root URL


if __name__ == '__main__':
    app.run(debug=True, host=local_ip, port=5000)
