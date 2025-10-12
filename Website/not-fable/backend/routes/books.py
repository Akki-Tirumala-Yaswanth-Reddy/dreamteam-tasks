from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from googleAPI.api import getGoogleBooks, getGoogleBook
from models.models import *
from dbAPI.bookDB import *
from dbAPI.reviewDB import *

books_bp = Blueprint('books', __name__)


@books_bp.get('/getbooks')
def GetBooks():
    try:
        data = request.args.to_dict()
        # I unexpectedly wrote the api in the best possible way.
        # The query parameters will be a dictionary, so i can directly pass them
        res = getGoogleBooks(**data)
        return jsonify({'ok': True, 'message': res}), 200
    except Exception as e:
        return jsonify({"ok":False, "error": "Could not fetch the data"}), 500
    
@books_bp.get('/getbook/<id>')
def GetBook(id):
    try:
        book_data = getGoogleBook(id)
        return jsonify({'ok': True ,'message': book_data}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": "Cound not fetch the requested book"}), 500
    
@books_bp.post('/bookRating')
@jwt_required()
def AddBookRating():
    try:
        req = request.get_json()
        book = Book.objects(google_id=req['google_id']).first()
        if not book:
            book_info = getGoogleBook(req['google_id'])
            if not book_info:
                return jsonify({'ok': False, 'error': 'Book not found'}), 404
            ok, data, error = createBook(req['google_id'], book_info.get('title'))
            if not ok:
                return jsonify({'ok': False, 'error': error}), 500
                
        ok, data, error = addBookRating(
            google_id=req['google_id'], 
            user_id=get_jwt_identity(), 
            rating=req['rating']
        )
        if not ok:
            return jsonify({'ok': False ,'error': error}), 500
        else:
            return jsonify({'ok': True, 'message': 'Success'}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500
    
@books_bp.delete('/bookRating')
@jwt_required()
def BookRatingDelete():
    try:
        req = request.get_json()
        ok, data, error = removeBookRating(req["google_id"], get_jwt_identity())
        if not ok:
            return jsonify({'ok': False, 'error': error}), 500
        else:
            return jsonify({'ok': True, 'message': 'Success'}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500
    
@books_bp.get('/bookRating/<id>')
def GetBookRatings(id):
    try:
        ok , data, error = getBookRatings(id)
        if not ok:
            return jsonify({'ok': False, 'error': error}), 500
        else:
            return jsonify({'ok': True, 'message': data}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500
    
@books_bp.get('/bookRating/<id>/<userid>')
@jwt_required()
def GetUserBookRating(id):
    try:
        ok, data, error = getUserBookRating(google_id=id, user_id=get_jwt_identity())
        if not ok: 
            return jsonify({'ok': False, 'error': error}), 500
        else: 
            return jsonify({'ok': True, 'message': data}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@books_bp.post('/bookReview')
@jwt_required()
def PostBookReview():
    try:
        req = request.get_json()
        print(req)
        if not all(key in req for key in ['google_id', 'heading', 'content', 'rating']):
            return jsonify({'ok': False, 'error': 'Missing required fields'}), 400
            
        book = Book.objects(google_id=req['google_id']).first()
        if not book:
            print(req['google_id'])
            book_info = getGoogleBook(req['google_id'])
            print(book_info)
            
            if not book_info:
                return jsonify({'ok': False, 'error': 'Book not found or API error'}), 404
                
            ok, data, error = createBook(req['google_id'], book_info.get('title'))
            print(ok, data, error)
            if not ok:
                return jsonify({'ok': False, 'error': error}), 500
                
        ok, review_id, error = createReview(
            get_jwt_identity(), 
            req['google_id'], 
            req['heading'], 
            req['content'], 
            req['rating']
        )
        print(ok, review_id, error)
        if not ok:
            return jsonify({'ok': False, 'error': error}), 500
        else: 
            return jsonify({'ok': True, 'message': {'ok': True}}), 200
        
    except Exception as e:
        print(str(e))
        return jsonify({'ok': False, 'error': str(e)}), 500

@books_bp.delete('/bookReview')
@jwt_required()
def DeleteBookReview():
    try:
        req = request.get_json()
        ok, data, error = deleteReview(req['review_id'], get_jwt_identity())
        if not ok:
            return jsonify({'ok': False, 'error': error}), 500
        else:
            return jsonify({'ok': True, 'message': "Review deleted successfully"}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500
    
@books_bp.get('/bookReview/<id>')
def GetBookReviews(id):
    try:
        ok , data, error = getBookReviews(id)
        print(data)
        if not ok:
            return jsonify({'ok': False, 'error': error}), 500
        else:
            return jsonify({'ok': True, 'message': data}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@books_bp.get('/bookReview/<id>/<userid>')
@jwt_required()
def GetUserBookReview(id, userId):
    try:
        ok, data, error = getUserBookReview(google_id=id, user_id=get_jwt_identity())
        if not ok: 
            return jsonify({'ok': False, 'error': error}), 500
        else: 
            return jsonify({'ok': True, 'message': data}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500