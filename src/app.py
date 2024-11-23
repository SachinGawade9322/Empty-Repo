import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.authentication import register, login, logout
from models.profile_update import update_user_details, get_user_details, update_profile_photo
from models.freelancer_application import get_all_applications
from models.client_project import create_project, get_client_project_details, get_client_project_by_id
from recommandation_system import recommend

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

def handle_errors(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return wrapper

@app.route('/register', methods=['POST'])
@handle_errors
def register_route():
    return register()

@app.route('/login', methods=['POST'])
@handle_errors
def login_route():
    return login()

@app.route('/logout', methods=['POST'])
@handle_errors
def logout_route():
    return logout()

@app.route('/update_user_details', methods=['POST'])
@handle_errors
def update_user_details_route():
    return update_user_details()

@app.route('/get_user_details', methods=['GET'])
@handle_errors
def get_user_details_route():
    return get_user_details()

@app.route('/update_profile_photo', methods=['POST'])
@handle_errors
def update_profile_photo_route():
    return update_profile_photo()

@app.route('/apply', methods=['POST'])
@handle_errors
def apply_for_work_route():
    return apply_for_work()

@app.route('/create_project', methods=['POST'])
@handle_errors
def create_project_route():
    return create_project()

@app.route('/get_project_details', methods=['GET'])
@handle_errors
def get_project_details_route():
    return get_client_project_details()

@app.route('/get_project_details/<int:project_id>', methods=['GET'])
@handle_errors
def get_project_details_id_route(project_id):
    return get_client_project_by_id(project_id)

@app.route('/recommend', methods=['POST'])
@handle_errors
def recommandation_route():
    data = request.get_json()
    project_id = data.get('project_id')
    if not project_id:
        return jsonify({"error": "Project ID is required."}), 400
    return recommend(project_id)

# Health Check Route
@app.route('/health', methods=['GET'])
@handle_errors
def health_check():
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(debug=True) 