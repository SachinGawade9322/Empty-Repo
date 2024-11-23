from flask import Blueprint
from controller.client_ProjectsController import create_client_project, get_all_client_projects

client_projects_bp = Blueprint('client_projects', __name__)

client_projects_bp.route('/', methods=['POST'])(create_client_project)
client_projects_bp.route('/', methods=['GET'])(get_all_client_projects)