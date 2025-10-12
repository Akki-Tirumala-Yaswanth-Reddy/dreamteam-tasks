from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from dbAPI.socialDB import *

social_bp = Blueprint('social', __name__)

@social_bp.post('/follower')
@jwt_required()
def AddFollower():
    req = request.get_json()
    ok, data, error = addFollower(get_jwt_identity(), req['follower_id'])
    if ok:
        return jsonify({'ok': True, 'message': data})
    else:
        return jsonify({'ok': False, 'error': error})

@social_bp.delete('/follower')
@jwt_required()
def RemoveFollower():
    req = request.get_json()
    ok, data, error = removeFollower(get_jwt_identity(), req['follower_id'])
    if ok:
        return jsonify({'ok': True, 'message': data})
    else:
        return jsonify({'ok': False, 'error': error})

@social_bp.get('/followers')
@jwt_required()
def GetUsersFollowers():
    ok , data, error = getFollowers(get_jwt_identity())
    if ok:
        return jsonify({'ok': True, 'message': data})
    else:
        return jsonify({'ok': False, 'error': error})

@social_bp.get('/following')
@jwt_required()
def GetUsersFollowing():
    ok , data, error = getFollowing(get_jwt_identity())
    if ok:
        return jsonify({'ok': True, 'message': data})
    else:
        return jsonify({'ok': False, 'error': error})