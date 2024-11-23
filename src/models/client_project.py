from flask import request, jsonify
from models.client_project import ClientProject
from utils.connection import get_db_connection

def create_project():
    data = request.get_json()
    user_id = data.get('user_id')
    project_title = data.get('project_title')
    project_description = data.get('project_description')
    project_link = data.get('project_link')

    if not user_id or not project_title or not project_description or not project_link:
        return jsonify({"error": "User  ID, project title, description, and link are required."}), 400

    project_id = ClientProject.create_client_project(user_id, project_title, project_description, project_link)

    return jsonify({"message": "Project created successfully.", "project_id": project_id}), 201

def get_client_project_details():
    projects = ClientProject.get_all_client_projects()
    
    return jsonify({"projects": projects}), 200

def get_client_project_by_id(project_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM client_projects WHERE id = %s", (project_id,))
    project = cur.fetchone()
    cur.close()
    conn.close()

    if project is None:
        return jsonify({"error": "Project not found."}), 404

    project_details = {
        "id": project[0],
        "user_id": project[1],
        "project_title": project[2],
        "project_description": project[3],
        "project_link": project[4]
    }

    return jsonify(project_details), 200