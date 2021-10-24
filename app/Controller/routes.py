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
bp_routes.static_folder = Config.STATIC_FOLDER

@bp_routes.route('/', methods=['GET','POST'])
@bp_routes.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    positions = Position.query.all()
    print("Positions", positions)
    return render_template('index.html', research_positions=positions)

'''
@bp_routes.route('/position/<pos_id>', methods=['GET','POST'])
@login_required
def singlePosition():
    def displayPosition(pos_id):
        position = Position.query.filter_by(id=pos_id).first()
    return render_template('position.html', position=position)
'''

@bp_routes.postPosition('postposition', methods=['GET', 'POST'])
@login_required
def postPosition():
    pForm = PositionForm()
    if pForm.validate_on_submit():
        position = Position(title=pForm.title.data, description=pForm.description.data, start_date=pForm.start_date.data, 
                            end_date=pForm.end_date.data, time_commitment=pForm.time_commitment.data,
                            faculty_id=pForm.faculty_id.data, required_qualification=pForm.required_qualifications.data,
                            research_fields=pForm.research_fields.data, students=pForm.students.data)
        db.session.add(position)
        db.session.commit()
        flash('You have created a position!')
        return redirect(url_for('routes.index'))
    return render_template('create.html', form=pForm)
        
