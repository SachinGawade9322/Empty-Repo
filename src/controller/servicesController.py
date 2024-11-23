from flask import jsonify, request
from models.service import Service

def create_service():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    price = data.get('price')

    if not title or not description or price is None:
        return jsonify({"error": "All fields are required"}), 400

    service_id = Service.create_service(title, description, price)
    return jsonify({"message": "Service created", "id": service_id}), 201

def get_all_services():
    services = Service.get_all_services()
    return jsonify(services), 200