from flask import Blueprint
from controller.freelancer_ApplicationsController import create_freelancer_application, get_all_freelancer_applications

freelancer_applications_bp = Blueprint('freelancer_applications', __name__)

freelancer_applications_bp.route('/', methods=['POST'])(create_freelancer_application)
freelancer_applications_bp.route('/', methods=['GET'])(get_all_freelancer_applications)