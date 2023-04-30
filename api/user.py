import datetime
import uuid
from utils.decorator import token_required
from flask import request, jsonify, make_response, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import db, User

user_api = Blueprint('user_api', __name__)


# User endpoints

# Create admin user
@user_api.route('/admin', methods=['POST'])
def create_admin_user():
    
    # Check if SuperAdmin already exists
    if User.query.filter_by(username="SuperAdmin").first() is not None:
        return jsonify({'message' : 'SuperAdmin already exists'}), 409
    
    hashed_password = generate_password_hash("SuperPassword", method='sha256')
    
    new_user = User(public_id=str(uuid.uuid4()), username="SuperAdmin", password=hashed_password, is_admin=True)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message' : 'SuperAdmin created'})

# Updtae password user

@user_api.route('/admin', methods=['PUT'])
@token_required
def update_admin_password(current_user):
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})    
    
    # Retrieve the SuperAdmin user
    superadmin_user = User.query.filter_by(username="SuperAdmin").first()

    # Check if SuperAdmin user exists
    if superadmin_user is None:
        return jsonify({'message' : 'SuperAdmin does not exist'}), 404

    # Get the new password from the request body
    new_password = request.json.get('new_password')

    # Check if new_password is provided
    if not new_password:
        return jsonify({'message' : 'New password is missing'}), 400

    # Generate new hashed password and update it in the database
    hashed_password = generate_password_hash(new_password, method='sha256')
    superadmin_user.password = hashed_password
    db.session.commit()

    return jsonify({'message' : 'SuperAdmin password updated'})


# Show all users
@user_api.route('/user', methods=['GET'])
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
@user_api.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):
    
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    
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
@user_api.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    
    data = request.get_json()
    
    hashed_password = generate_password_hash(data['password'], method='sha256')
    
    new_user = User(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password, is_admin=False)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message' : 'New user created'})

# Update user
@user_api.route('/user/<public_id>', methods=['PUT'])
@token_required
def update_user(current_user, public_id):
    
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})
    
    user = User.query.filter_by(public_id=public_id).first()
    
    if not user:
        return jsonify({'message' : 'User not found'})

    user.is_admin = True
    db.session.commit()

    return jsonify({'message' : 'The user has been updated!'})

# Delete user
@user_api.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    
    if not current_user.is_admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    if user.is_admin and user.username == 'SuperAdmin':
        return jsonify({'message' : 'Cannot delete SuperAdmin!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'})

# Login
@user_api.route('/login')
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