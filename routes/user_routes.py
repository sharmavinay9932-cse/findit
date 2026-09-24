from flask import Blueprint, jsonify, session, request
from services.auth_service import AuthService
from services.item_service import ItemService

user_bp = Blueprint('user', __name__)
auth_service = AuthService()
item_service = ItemService()

@user_bp.route('/me', methods=['GET'])
def get_me():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Not authenticated", "errors": {}}), 401
    user = auth_service.get_user_by_id(session['user_id'])
    return jsonify({"success": True, "message": "User fetched", "data": user}), 200

@user_bp.route('/items', methods=['GET'])
def get_user_items():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Not authenticated", "errors": {}}), 401
    items = item_service.get_items_by_user(session['user_id'])
    return jsonify({"success": True, "message": "User items fetched", "data": items}), 200
