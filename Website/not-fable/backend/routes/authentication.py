from flask import Blueprint, jsonify, request
from models.models import User
from mongoengine import NotUniqueError
from extension import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token

# "Registering" the routes
login_bp = Blueprint('login', __name__)
signup_bp = Blueprint('signup', __name__)

# Signup
@signup_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']

    # Some validation for the incoming data
    if len(password) < 8:
        return jsonify({'error': 'Password must be atleast 8 characters long'}), 400 # All the reponse codes are in an md file
    
    if str(email).find('@') == -1 or str(email).find('.com') == -1:
        return jsonify({'error': 'Format of the email is wrong'}), 400
    
    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password, email=email)
        user.save()
        return jsonify({'message': 'User has been created'}), 201
    except NotUniqueError:
        return jsonify({'error': 'This username is taken'}), 409
    except Exception as e:
        return jsonify({'error': 'Server error:' + str(e)}), 500

# Login
@login_bp.post('/login') # We can directly use post like in express.js
def login():
    data = request.get_json()
    if len(data['username']) == 0 or len(data['password']) == 0:
        return jsonify({'error': "Username or password is empty"}), 400
    try:
        user_db = User.objects(username=data['username']).first()
        if not user_db:
            return jsonify({'error': "User is not found"}), 404
        elif bcrypt.check_password_hash(user_db.password, data['password']):
            access_token = create_access_token(identity=str(user_db.id))
            refresh_token = create_refresh_token(identity=str(user_db.id))
            return jsonify({'message': "Success, the user has been logged in",
                            'access_token': access_token,
                            'refresh_token': refresh_token,
                            'user_id': str(user_db.id)
                            }), 200
        return jsonify({'error': "Given password is wrong."}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@login_bp.post('/refresh')
@jwt_required(refresh=True)
def refresh():
    try:
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return jsonify({
            'access_token': new_access_token,
            'message': 'Token refreshed successfully'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
