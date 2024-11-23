from flask import Blueprint
from controller.portfoliosController import create_portfolio, get_all_portfolios

portfolios_bp = Blueprint('portfolios', __name__)

portfolios_bp.route('/', methods=['POST'])(create_portfolio)
portfolios_bp.route('/', methods=['GET'])(get_all_portfolios)