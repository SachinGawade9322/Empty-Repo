from flask import Blueprint
from controller.profile_UpdateController import create_profile_update, get_all_profile_updates

profile_update_bp = Blueprint('profile_update', __name__)

profile_update_bp.route('/', methods=['POST'])(create_profile_update)
profile_update_bp.route('/', methods=['GET'])(get_all_profile_updates)