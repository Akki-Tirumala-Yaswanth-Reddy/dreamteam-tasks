from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import User
from dbAPI.reviewDB import *

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.post('/review/<review_id>')
@jwt_required()
def ChangeReview(review_id):
    try:
        req = request.get_json()
        ok, data, error = changeReview(review_id, req['content'], get_jwt_identity())
        if not ok:
            return jsonify({'ok': False, 'error': error}), 500
        else:
            return jsonify({'ok': True, 'message': 'Review updated successfully'}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@reviews_bp.get('/review/<review_id>')
@jwt_required()
def GetReview(review_id):
    try:
        print(review_id)
        ok, data, error = getReview(review_id)
        print(data)
        if not ok:
            return jsonify({'ok': False, 'error': error}), 500
        else:
            return jsonify({'ok': True, 'message': data}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500
    
@reviews_bp.get('/review/user')
@jwt_required()
def GetReviewByUser():
    try:
        ok, data, error = getUserReviews(user_id=get_jwt_identity())
        if not ok:
            return jsonify({'ok': False, 'error': error}), 500
        else:
            return jsonify({'ok': True, 'message': data}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@reviews_bp.delete('/review/<review_id>')
@jwt_required()
def DeleteReview(review_id):
    try:
        ok, data, error = deleteReview(review_id, get_jwt_identity())
        if not ok:
            return jsonify({'ok': False, 'error': error}), 500
        else:
            return jsonify({'ok': True, 'message': 'Review deleted successfully'}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@reviews_bp.post('/review/<review_id>/like')
@jwt_required()
def AddLike(review_id):
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'ok': False, 'error': 'User not found'}), 404
        
        ok, data, error = addLike(user_id, review_id)
        if not ok:
            return jsonify({'ok': False, 'error': error}), 500
        else:
            return jsonify({'ok': True, 'message': data}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@reviews_bp.post('/review/<review_id>/dislike')
@jwt_required()
def AddDislike(review_id):
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'ok': False, 'error': 'User not found'}), 404
        
        ok, data, error = addDislike(user_id, review_id)
        if not ok:
            return jsonify({'ok': False, 'error': error}), 500
        else:
            return jsonify({'ok': True, 'message': data}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@reviews_bp.delete('/review/<review_id>/likedislike')
@jwt_required()
def RemoveLikeDislike(review_id):
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'ok': False, 'error': 'User not found'}), 404
        
        ok, data, error = removeLikeDislike(user_id, review_id)
        if not ok:
            return jsonify({'ok': False, 'error': error}), 500
        else:
            return jsonify({'ok': True, 'message': data}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@reviews_bp.post('/review/<review_id>/comment')
@jwt_required()
def AddComment(review_id):
    try:
        req = request.get_json()
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'ok': False, 'error': 'User not found'}), 404
        
        ok, data, error = addComment(user_id, review_id, req['content'])
        if not ok:
            return jsonify({'ok': False, 'error': error}), 500
        else:
            return jsonify({'ok': True, 'message': 'Comment added successfully'}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@reviews_bp.delete('/review/<review_id>/comment/<comment_id>')
@jwt_required()
def DeleteComment(review_id, comment_id):
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'ok': False, 'error': 'User not found'}), 404
        
        ok, data, error = deleteComment(user_id, review_id, comment_id)
        if not ok:
            return jsonify({'ok': False, 'error': error}), 500
        else:
            return jsonify({'ok': True, 'message': data}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500
