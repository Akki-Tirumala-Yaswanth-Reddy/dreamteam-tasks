from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from dbAPI.listDB import *

lists_bp = Blueprint('lists', __name__)

@lists_bp.post('/list')
@jwt_required()
def CreateList():
    try:
        req = request.get_json()        
        success, list_data, error = createList(req.get('name'), get_jwt_identity())
        if not success:
            return jsonify({'ok': False, 'message': None, 'error': error}), 400
        return jsonify({'ok': True, 'message': list_data, 'error': None}), 201
        
    except Exception as e:
        
        return jsonify({'ok': False, 'message': None, 'error': 'Internal server error'}), 500

@lists_bp.get('/lists')
@jwt_required()
def GetUserLists():
    try:
        success, lists_data, error = getUserLists(get_jwt_identity())
        if not success:
            return jsonify({'ok': False, 'message': None, 'error': error}), 400
        return jsonify({'ok': True, 'message': lists_data, 'error': None})
    except Exception as e:
        print(e)
        return jsonify({'ok': False, 'message': None, 'error': 'Internal server error'}), 500

@lists_bp.get('/list/<list_id>')
@jwt_required()
def GetListById(list_id):
    try:
        success, list_data, error = getListById(list_id)
        if not success:
            return jsonify({'ok': False, 'message': None, 'error': error}), 400
        return jsonify({'ok': True, 'message': list_data, 'error': None})
        
    except Exception as e:
        return jsonify({'ok': False, 'message': None, 'error': 'Internal server error'}), 500

@lists_bp.post('/list/<list_id>/book')
@jwt_required()
def AddBookToList(list_id):
    try:
        req = request.get_json()
        success, list_data, error = addBookToList(list_id, req.get('google_id'), req.get('title'))
        
        if not success:
            return jsonify({'ok': False, 'message': None, 'error': error}), 400
        
        return jsonify({'ok': True, 'message': list_data, 'error': None})
        
    except Exception as e:
        return jsonify({'ok': False, 'message': None, 'error': 'Internal server error'}), 500

@lists_bp.delete('/list/<list_id>/book/<google_id>')
@jwt_required()
def RemoveBookFromList(list_id, google_id):
    try:
        success, list_data, error = removeBookFromList(list_id, google_id)
        if not success:
            return jsonify({'ok': False, 'message': None, 'error': error}), 400
        
        return jsonify({'ok': True, 'message': list_data, 'error': None})
        
    except Exception as e:
        return jsonify({'ok': False, 'message': None, 'error': 'Internal server error'}), 500

@lists_bp.delete('/list/<list_id>')
@jwt_required()
def DeleteList(list_id):
    try:
        success, message, error = deleteList(list_id, get_jwt_identity())
        if not success:
            return jsonify({'ok': False, 'message': None, 'error': error}), 400
        
        return jsonify({'ok': True, 'message': message, 'error': None})
        
    except Exception as e:
        return jsonify({'ok': False, 'message': None, 'error': 'Internal server error'}), 500