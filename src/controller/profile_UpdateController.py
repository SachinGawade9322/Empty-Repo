from flask import jsonify, request
from models.profile_update import ProfileUpdate
from flask_jwt_extended import jwt_required, get_jwt_identity

@jwt_required()
def create_profile_update():
    current_user = get_jwt_identity()
    data = request.get_json()
    updated_info = data.get('updated_info')

    if not updated_info:
        return jsonify({"error": "Updated information is required"}), 400

    update_id = ProfileUpdate.create_update(current_user['user_id'], updated_info)
    return jsonify({"message": "Profile update created", "id": update_id}), 201

@jwt_required()
def get_all_profile_updates():
    updates = ProfileUpdate.get_all_updates()
    return jsonify(updates), 200