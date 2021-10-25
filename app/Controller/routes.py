from flask import Blueprint
from config import Config
from flask_login import current_user, login_required
from app.Model.position_models import Position
from app.Model.user_models import User
from flask import render_template, flash, redirect, url_for, request
from app import db
from flask_login import current_user, login_user, logout_user, login_required
from app.Controller.position_forms import CreatePositionForm

import app.Model.user_models as user_models
from datetime import datetime

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'
bp_routes.static_folder = Config.STATIC_FOLDER

## FUTURE: With faculty, sort so faculty id is on top? Or only show faculty's post?
@bp_routes.route('/', methods=['GET','POST'])
@bp_routes.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    positions = Position.query.all()
    return render_template('index.html', research_positions=positions)


@bp_routes.route('/position/<pos_id>', methods=['GET','POST'])
@login_required
def display_position(pos_id):
    position = Position.query.filter_by(id=int(pos_id)).first()
    return render_template('position.html', position=position)


@bp_routes.route('/create_position', methods=['GET', 'POST'])
@login_required
def create_position():

    if type(current_user) != user_models.Faculty:
        flash('Access Denied: not logged in as Faculty')
        return redirect(url_for('routes.index'))

    pform = CreatePositionForm()
    if pform.validate_on_submit():
        start_date  = datetime.strptime(pform.start_data.data, '%m/%d/%Y')
        end_date    = datetime.strptime(pform.end_date.data, '%m/%d/%Y')

        position = Position(title       = pform.title.data,
                            description = pform.description.data,
                            start_date  = start_date,
                            end_date    = end_date,
                            faculty_id  = current_user.id,
                            time_commitment         = int(pform.time_commitment.data),
                            required_qualification  = pform.required_qualifications.data,
                            research_fields         = [x for x in pform.research_fields.data]
                            )

        position.save_to_db()
        flash('Position successfully created.')
        return redirect(url_for('routes.index'))

    return render_template('create.html', form=pform)
