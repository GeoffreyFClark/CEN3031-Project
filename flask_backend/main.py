from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from flask_sqlalchemy import SQLAlchemy  # When using VSCode I had an issue with resolving this import and realized I had to manually switch my python interpreter from system to the venv interpreter
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash, check_password_hash


# Initialize the Flask app
app = Flask(__name__)

# CORS = Cross Origin Resource Sharing to allow interaction between our frontend and backend
# This is fine for development, but for production we need to restrict to our frontend domain for security:
# CORS(app, resources={r"/api/*": {"origins": "http://OurFrontendDomain.com"}})
CORS(app)  

# Configuration of the SQLite database for user data
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CommuniCare_Users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configuration of JWT (JSON Web Tokens) for user authentication
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')  
jwt = JWTManager(app)

# Currently planning to store community resources in a JSON file
with open('resources.json', 'r') as file:
    resources = json.load(file)


# --------- Database Models ---------

# User model for the SQLite database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# --------- API Endpoints ---------

@app.route('/api/resources', methods=['GET'])
def get_resources():
    return jsonify(resources)

@app.route('/api/resources', methods=['POST'])
def add_resource():
    new_resource = request.json
    resources.append(new_resource)
    save_resources()
    return jsonify(new_resource), 201

@app.route('/api/resources/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    resource = next((r for r in resources if r["id"] == resource_id), None)
    if not resource:
        return jsonify({"message": "Resource not found"}), 404
    update_data = request.json
    resource.update(update_data)
    save_resources()
    return jsonify(resource)

@app.route('/api/resources/<int:resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    """
    Delete a resource by its ID.
    """
    global resources
    resources = [r for r in resources if r["id"] != resource_id]
    save_resources()
    return jsonify({"message": "Resource deleted"})


# -------------------------------


def save_resources():
    """
    Save the resources to the JSON file.
    """
    with open('resources.json', 'w') as file:
        json.dump(resources, file, indent=2)



if __name__ == '__main__':
    app.run(debug=True)