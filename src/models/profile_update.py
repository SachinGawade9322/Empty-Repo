from flask import request, jsonify
from models.profile_update import ProfileUpdate

def update_user_details():
    data = request.get_json()
    user_id = data.get('user_id')
    updated_info = data.get('updated_info')

    if not user_id or not updated_info:
        return jsonify({"error": "User  ID and updated info are required."}), 400

    # Call the method to create an update
    update_id = ProfileUpdate.create_update(user_id, updated_info)
    
    return jsonify({"message": "Profile updated successfully.", "update_id": update_id}), 200

def get_user_details():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "User  ID is required."}), 400

    user_details = {
        "user_id": user_id,
        "name": "John Doe",  # Example data
        "email": "john.doe@example.com"  
    }

    return jsonify(user_details), 200

def update_profile_photo():
    data = request.get_json()
    user_id = data.get('user_id')
    profile_photo = data.get('profile_photo')  # just for reference we can change according

    if not user_id or not profile_photo:
        return jsonify({"error": "User  ID and profile photo are required."}), 400

    return jsonify({"message": "Profile photo updated successfully."}), 200