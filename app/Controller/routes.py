from flask import Blueprint
from config import Config
from flask_login import current_user, login_required
from app.Model.position_models import Position
from app.Model.user_models import User
from flask import render_template, flash, redirect, url_for, request
from app import db
from flask_login import current_user, login_user, logout_user, login_required

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'

@bp_routes.route('/', methods=['GET','POST'])
@bp_routes.route('/index', methods=['GET', 'POST'])
def index():
    
    positions = Position.query.all()
    
    return render_template('index.html', research_positions=positions)