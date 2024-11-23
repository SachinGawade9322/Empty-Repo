from flask import Blueprint
from controller.servicesController import create_service, get_all_services

services_bp = Blueprint('services', __name__)

services_bp.route('/', methods=['POST'])(create_service)
services_bp.route('/', methods=['GET'])(get_all_services)