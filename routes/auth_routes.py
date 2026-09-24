from flask import Blueprint, request, jsonify, session
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    success, result = auth_service.register_user(data)
    if success:
        return jsonify({"success": True, "message": "Registration successful", "data": result}), 201
    return jsonify({"success": False, "message": result, "errors": {}}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    success, result = auth_service.authenticate_user(data.get('email'), data.get('password'))
    if success:
        session['user_id'] = result['id']
        return jsonify({"success": True, "message": "Login successful", "data": result}), 200
    return jsonify({"success": False, "message": result, "errors": {}}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"success": True, "message": "Logged out successfully", "data": {}}), 200

@auth_bp.route('/me', methods=['GET'])
def me():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Not authenticated", "errors": {}}), 401
    user = auth_service.get_user_by_id(session['user_id'])
    if user:
        return jsonify({"success": True, "message": "User fetched", "data": user}), 200
    return jsonify({"success": False, "message": "User not found", "errors": {}}), 404
