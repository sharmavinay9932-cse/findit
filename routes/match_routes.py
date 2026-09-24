from flask import Blueprint, jsonify, session
from services.match_service import MatchService

match_bp = Blueprint('match', __name__)
match_service = MatchService()

@match_bp.route('/<lost_item_id>', methods=['GET'])
def get_matches(lost_item_id):
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Not authenticated", "errors": {}}), 401
        
    matches = match_service.find_potential_matches(lost_item_id)
    return jsonify({"success": True, "message": "Matches found", "data": matches}), 200
