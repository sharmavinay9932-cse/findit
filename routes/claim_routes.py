from flask import Blueprint, request, jsonify, session
from repositories.claim_repository import ClaimRepository

claim_bp = Blueprint('claim', __name__)
claim_repo = ClaimRepository()

@claim_bp.route('', methods=['POST'])
def create_claim():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Not authenticated", "errors": {}}), 401
    
    data = request.json
    result = claim_repo.create_claim(data.get('match_id'), session['user_id'], data.get('verification_answer'))
    
    if result:
        return jsonify({"success": True, "message": "Claim submitted successfully", "data": result}), 201
    return jsonify({"success": False, "message": "Failed to submit claim", "errors": {}}), 400

@claim_bp.route('', methods=['GET'])
def get_claims():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Not authenticated", "errors": {}}), 401
    
    # In a real app, fetch role from DB. For now pass 'user'.
    claims = claim_repo.get_claims(session['user_id'], role='user')
    return jsonify({"success": True, "message": "Claims fetched", "data": claims}), 200

@claim_bp.route('/<claim_id>', methods=['PUT'])
def update_claim(claim_id):
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Not authenticated", "errors": {}}), 401
    
    data = request.json
    status = data.get('status')
    
    if claim_repo.update_claim_status(claim_id, status):
        return jsonify({"success": True, "message": f"Claim status updated to {status}", "data": {}}), 200
    return jsonify({"success": False, "message": "Failed to update claim", "errors": {}}), 400
