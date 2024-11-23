from flask import jsonify, request
from models.freelancer_application import FreelancerApplication
from flask_jwt_extended import jwt_required, get_jwt_identity

@jwt_required()
def create_freelancer_application():
    current_user = get_jwt_identity()
    data = request.get_json()
    application_details = data.get('application_details')

    if not application_details:
        return jsonify({"error": "Application details are required"}), 400

    application_id = FreelancerApplication.create_application(current_user['user_id'], application_details)
    return jsonify({"message": "Freelancer application created", "id": application_id}), 201

@jwt_required()
def get_all_freelancer_applications():
    applications = FreelancerApplication.get_all_applications()
    return jsonify(applications), 200