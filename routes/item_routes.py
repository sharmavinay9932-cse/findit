from flask import Blueprint, request, jsonify, session
from services.item_service import ItemService

item_bp = Blueprint('item', __name__)
item_service = ItemService()

@item_bp.route('', methods=['GET'])
def get_items():
    items = item_service.get_all_items()
    # Apply basic filtering if needed here (e.g. status)
    return jsonify({"success": True, "message": "Items fetched", "data": items}), 200

@item_bp.route('/<item_id>', methods=['GET'])
def get_item(item_id):
    item = item_service.get_item(item_id)
    if item:
        return jsonify({"success": True, "message": "Item fetched", "data": item}), 200
    return jsonify({"success": False, "message": "Item not found", "errors": {}}), 404

@item_bp.route('/lost', methods=['POST'])
def report_lost():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Not authenticated", "errors": {}}), 401
    
    data = dict(request.form)
    data['user_id'] = session['user_id']
    file = request.files.get('photo')
    
    item = item_service.report_item('lost', data, file)
    return jsonify({"success": True, "message": "Lost item reported", "data": item}), 201

@item_bp.route('/found', methods=['POST'])
def report_found():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Not authenticated", "errors": {}}), 401
    
    data = dict(request.form)
    data['user_id'] = session['user_id']
    file = request.files.get('photo')
    
    item = item_service.report_item('found', data, file)
    return jsonify({"success": True, "message": "Found item reported", "data": item}), 201
