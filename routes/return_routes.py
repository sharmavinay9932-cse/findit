from flask import Blueprint, request, jsonify, session
from repositories.claim_repository import ClaimRepository

return_bp = Blueprint('return', __name__)
claim_repo = ClaimRepository()

@return_bp.route('', methods=['POST'])
def create_return():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Not authenticated", "errors": {}}), 401
    
    data = request.json
    claim_id = data.get('claim_id')
    received_by = data.get('received_by')
    confirmation = data.get('confirmation')
    
    # Using session['user_id'] as returned_by for this example
    if claim_repo.create_return(claim_id, session['user_id'], received_by, confirmation):
        return jsonify({"success": True, "message": "Return recorded successfully", "data": {}}), 201
    return jsonify({"success": False, "message": "Failed to record return", "errors": {}}), 400
