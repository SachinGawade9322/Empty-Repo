from flask import jsonify, request
from models.portfolio import Portfolio
from flask_jwt_extended import jwt_required, get_jwt_identity

@jwt_required()
def create_portfolio():
    current_user = get_jwt_identity()
    data = request.get_json()
    project_title = data.get('project_title')
    project_description = data.get('project_description')
    project_link = data.get('project_link')

    if not project_title or not project_description:
        return jsonify({"error": "All fields are required"}), 400

    portfolio_id = Portfolio.create_portfolio(current_user['user_id'], project_title, project_description, project_link)
    return jsonify({"message": "Portfolio created", "id": portfolio_id}), 201

@jwt_required()
def get_all_portfolios():
    portfolios = Portfolio.get_all_portfolios()
    return jsonify(portfolios), 200