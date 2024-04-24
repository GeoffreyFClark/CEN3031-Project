from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy  # When using VSCode I had an issue with resolving this import and realized I had to manually switch my python interpreter from system to the venv interpreter
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

#Local imports
from search import search_resources, search_by_id

DATASET_PATH = 'dataset.json'
ID_PATH = 'id.json'
USER_NOT_FOUND_MESSAGE = {"error": "User not found"}  # To satisfy SonarCloud test 

global resources
global current_id

# Initialize the Flask app
app = Flask(__name__)


# CORS = Cross Origin Resource Sharing to allow interaction between our frontend and backend
# This is fine for development, but for production we need to restrict to our frontend domain for security:
# CORS(app, resources={r"/api/*": {"origins": "http://OurFrontendDomain.com"}})
CORS(app)  

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CommuniCare_Users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')  
jwt = JWTManager(app)



user_resources = db.Table('user_resources',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('resource_id', db.Integer, db.ForeignKey('resource.id'), primary_key=True)
)



# ---------------------------------------- Database Models --------------------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    resources = db.relationship('Resource', secondary=user_resources, backref='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_resource_ids(self):
        return [resource.id for resource in self.resources]
    
class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)



# ------------------------------------ API Endpoints ----------------------------------------------

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
    if resources is None:
        return jsonify({"error": "Resources are not loaded"}), 500
    return jsonify(resources)

# Add new resource
@app.route('/api/resources', methods=['POST'])
@jwt_required()
def add_resource():
    global current_id
    try:
        new_resource = request.json
        resource_type = new_resource.get('type')
        resource_data = new_resource.get('resource')

        if not isinstance(resource_data, dict):
            raise ValueError("Resource data is not a dictionary.")

        if not resource_type or resource_type not in resources:
            raise ValueError(f"Invalid or missing resource type: {resource_type}")

        resource_data['id'] = current_id
        resource_data['date_added'] = datetime.now().strftime('%m/%d/%Y')
        current_id += 1
        resources[resource_type].append(resource_data)
        save_resources()

        # Save only the resource ID to the user database
        current_user_username = get_jwt_identity()
        user = User.query.filter_by(username=current_user_username).first()
        if not user:
            return jsonify(USER_NOT_FOUND_MESSAGE), 404

        resource = Resource(id=resource_data['id'])
        user.resources.append(resource)
        db.session.commit()

        return jsonify(resource_data), 201

    except Exception as e:
        print(f"Failed to add resource: {e}")
        return jsonify({"error": "Failed to add resource", "message": str(e)}), 500


@app.route('/api/my-resources', methods=['GET'])
@jwt_required()
def get_my_resources():
    current_user_username = get_jwt_identity()
    user = User.query.filter_by(username=current_user_username).first()
    if not user:
        return jsonify(USER_NOT_FOUND_MESSAGE), 404

    resources_response = get_resources() 
    user_resource_ids = user.get_resource_ids()

    user_resources = search_by_id(resources_response.json, user_resource_ids)

    return jsonify(user_resources), 200


@app.route('/api/resources/<int:resource_id>', methods=['PUT'])
@jwt_required()
def update_resource(resource_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    resource = Resource.query.filter_by(id=resource_id, users=user).first()

    if not resource:
        return jsonify({"error": "Resource not found"}), 404

    data = request.json
    resource.name = data.get('name', resource.name)
    resource.description = data.get('description', resource.description)
    db.session.commit()

    return jsonify({"message": "Resource updated"}), 200

@app.route('/api/resources/<int:resource_id>', methods=['DELETE'])
@jwt_required()
def delete_resource(resource_id):
    current_user_username = get_jwt_identity()
    user = User.query.filter_by(username=current_user_username).first()

    if not user:
        return jsonify(USER_NOT_FOUND_MESSAGE), 404

    resource = Resource.query.filter_by(id=resource_id).first()

    if not resource:
        return jsonify({"error": "Resource not found"}), 404

    if resource not in user.resources:
        return jsonify({"error": "Resource does not belong to the user"}), 403

    user.resources.remove(resource)
    db.session.commit()

    # Remove the resource from the dataset
    for resource_type in resources:
        resources[resource_type] = [r for r in resources[resource_type] if r['id'] != resource_id]
    save_resources()

    return jsonify({"message": "Resource deleted"}), 200


#Search endpoint for all users
@app.route('/api/search', methods=['POST'])
def search():
    criteria = request.json
    print("Flask | Initiating search type:", criteria)
    
    resources_response = get_resources() 
    
    results = search_resources(resources_response.json, criteria)
    print("Flask | Search results:", results)
    
    return jsonify(results)




# --------- Helper Functions ---------


# Save the resources to the dataset
def save_resources():
    try:
        with open(DATASET_PATH, 'w') as file:
            json.dump(resources, file, indent=4)
        with open(ID_PATH, 'w') as file:
            json.dump({'current_id': current_id}, file)
    except Exception as e:
        print(f"Failed to save resources or current ID: {e}")

def reinitialize_resources():
    global resources, current_id
    resources = {"Food bank": [], "Animal": [], "Veteran": [], "Substance abuse": []}
    current_id = 1

def load_resources():
    global resources, current_id
    try:
        with open(DATASET_PATH, 'r') as file:
            resources = json.load(file)
        
        with open(ID_PATH, 'r') as file:
            current_id_data = json.load(file)
            current_id = current_id_data['current_id']

        print("Resources and current_id loaded successfully.")
    except FileNotFoundError:
        print(f"Files not found. Working directory: {os.getcwd()}")
        reinitialize_resources()
        save_resources()  # To create initial files and avoid further load errors
    except json.JSONDecodeError:
        print("JSON decode error. Reinitializing structures.")
        reinitialize_resources()
        save_resources()
    except Exception as e:
        print(f"An unexpected error occurred while loading resources: {e}")
        reinitialize_resources()
        save_resources()





if __name__ == '__main__':
    with app.app_context():
        #db.drop_all() #You need to run this because I've changed the db models
        db.create_all()
    load_resources()  # Properly initialize resources and current_id
    app.run(debug=True)

    