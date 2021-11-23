from flask.blueprints import Blueprint
from App.controllers.user import display_all_users

user_bp = Blueprint('user', __name__, template_folder='../templates')
user_bp.route('/api/users', methods=['GET'])(display_all_users)
