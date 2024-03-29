from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from flask_sqlalchemy import SQLAlchemy  # When using VSCode I had an issue with resolving this import and realized I had to manually switch my python interpreter from system to the venv interpreter
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
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
with open('dataset.json', 'r') as file:
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


# Register endpoint
@app.route('/api/register', methods=['POST'])
def register():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"message": "Username already exists"}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201


# Login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)

    return jsonify({"message": "Invalid username or password"}), 401


# JWT protected route test
@app.route('/api/protected', methods=['GET'])
@jwt_required()  # This decorator requires a valid JWT to access this route
def protected():
    return jsonify({"message": "This is a test of using a JWT protected route."})


# Get resources
@app.route('/api/resources', methods=['GET'])
def get_resources():
    return jsonify(resources)


# Add new resource
@app.route('/api/resources', methods=['POST'])
def add_resource():
    new_resource = request.json
    resources.append(new_resource)
    save_resources()
    return jsonify(new_resource), 201


# Update resource by ID
@app.route('/api/resources/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    resource = next((r for r in resources if r["id"] == resource_id), None)
    if not resource:
        return jsonify({"message": "Resource not found"}), 404
    update_data = request.json
    resource.update(update_data)
    save_resources()
    return jsonify(resource)


# Delete resource by ID
@app.route('/api/resources/<int:resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    global resources
    resources = [r for r in resources if r["id"] != resource_id]
    save_resources()
    return jsonify({"message": "Resource deleted"})



# --------- Helper Functions ---------


# Save the resources to the JSON file
def save_resources():
    with open('resources.json', 'w') as file:
        json.dump(resources, file, indent=2)


if __name__ == '__main__':
    # db.create_all() will create the database tables based on the models, if these tables don't already exist
    # if they already exist, it will not recreate them and will not modify them
    with app.app_context():
        db.create_all()

    app.run(debug=True)