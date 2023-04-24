from flask import Flask, request, jsonify
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Ingredient, init_app

app = Flask(__name__)
app.config.from_object(Config)

init_app(app)

# ENDPONTS

# home
@app.route('/', methods=['GET'])
def home():
    return "<h1>Welsh Academy</h1><p>Welsh Academy's API site.</p>"

# User endpoints

# Show all users
@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users' : output})

# Show one user
@app.route('/user/<user_id>', methods=['GET'])
def get_one_user():
    return ''

# Create user
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    
    hashed_password = generate_password_hash(data['password'], method='sha256')
    
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message' : 'New user created'})

# Update user
@app.route('/user/<user_id>', methods=['PUT'])
def update_user():
    return ''

# Delete user
@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user():
    return ''