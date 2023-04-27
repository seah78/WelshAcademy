import datetime
from flask import Flask, request, jsonify, make_response
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps

from config import Config
from models import db, User, Ingredient, init_app

app = Flask(__name__)
app.config.from_object(Config)

init_app(app)

# decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated



# ENDPONTS

# home
@app.route('/', methods=['GET'])
def home():
    return "<h1>Welsh Academy</h1><p>Welsh Academy's API site.</p>"

# User endpoints

# Create admin user
@app.route('/admin', methods=['POST'])
def create_admin_user():
    
    hashed_password = generate_password_hash("SuperPassword", method='sha256')
    
    new_user = User(public_id=str(uuid.uuid4()), username="SuperAdmin", password=hashed_password, is_admin=True)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message' : 'SuperAdmin created'})

# Show all users
@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['is_admin'] = user.is_admin
        output.append(user_data)

    return jsonify({'users' : output})

# Show one user
@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):
    
    user = User.query.filter_by(public_id=public_id).first()
    
    if not user:
        return jsonify({'message' : 'User not found'})
    
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['username'] = user.username
    user_data['password'] = user.password
    user_data['is_admin'] = user.is_admin
    
    return jsonify({'user' : user_data})

# Create user
@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    data = request.get_json()
    
    hashed_password = generate_password_hash(data['password'], method='sha256')
    
    new_user = User(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password, is_admin=False)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message' : 'New user created'})

# Update user
@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def update_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()
    
    if not user:
        return jsonify({'message' : 'User not found'})

    user.is_admin = True
    db.session.commit()

    return jsonify({'message' : 'The user has been updated!'})

# Delete user
@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'})

# Login
@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
