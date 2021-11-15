from flask import Blueprint
from config import Config
from flask_login import current_user, login_required
from app.Model.position_models import Position, Application
from app.Model.user_models import User
from flask import render_template, flash, redirect, url_for, request
from app import db
from flask_login import current_user, login_user, logout_user, login_required
from app.Controller.position_forms import CreatePositionForm
from app.Controller.application_forms import ApplicationForm
from app.Controller.edit_forms import EditForm

import app.Model.user_models as user_models
from datetime import datetime

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'
bp_routes.static_folder = Config.STATIC_FOLDER

## FUTURE: With faculty, sort so faculty id is on top? Or only show faculty's post?
@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index', methods=['GET'])
@login_required
def index():
    positions = Position.query.all()
    return render_template('index.html', research_positions=positions)

@bp_routes.route('/position/<pos_id>', methods=['GET'])
@login_required
def display_position(pos_id):
    position = Position.query.filter_by(id=int(pos_id)).first()
    user = User.query.filter_by(id=position.faculty_id).first()
    return render_template('position.html', position=position, user=user)

@bp_routes.route('/view_applicants', methods=['GET'])
@login_required
def view_applicants():
    if not current_user.is_faculty():
        flash('Access Denied: not logged in as Faculty')
        return redirect(url_for('routes.index'))
    
    positions = Position.query.filter_by(faculty_id=current_user.id)
    
    return render_template('faculty_positions.html', positions=positions)

@bp_routes.route('/student/<student_id>', methods=['GET'])
@login_required
def display_applicant_info(student_id):
    if not current_user.is_faculty():
        flash('Access Denied: not logged in as Faculty')
        return redirect(url_for('routes.index'))
    
    student = User.query.filter_by(id=int(student_id)).first()
    
    return render_template('student.html', student=student)
    
@bp_routes.route('/apply/<pos_id>', methods=['GET', 'POST'])
@login_required
def apply(pos_id):
    if current_user.is_faculty():
        flash('Access Denied: You must be logged in as a student to apply for a position.')
        return redirect(url_for('routes.index'))
    
    appForm = ApplicationForm()

    if appForm.validate_on_submit():
        application = Application(description=appForm.description, ref_name=appForm.ref_name,
                                    ref_email = appForm.ref_email, position_id=pos_id,
                                    student_id=current_user.id)
        application.save_to_db()
        flash('Application successfully submitted.')
        return redirect(url_for('routes.index'))
    
    return render_template('apply.html', form=appForm)
    
@bp_routes.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():

    if current_user.is_faculty():
        flash('Access Denied: You must be logged in as a student to apply for a position.')
        return redirect(url_for('routes.index'))

    user = User.query.filter_by(id = current_user.id).first()
    print(f'Type of user: {type(user)}')

    eForm = EditForm()
    # eForm.first_name.data           = user.first_name
    # eForm.major.data                = user.major
    # eForm.cum_GPA.data              = user.gpa
    # eForm.grad_date.data            = user.graduation_date
    # eForm.languages.data            = user.programming_languages
    # #eForm.prior_experience.data     = user.research_experience
    # eForm.research_topics.data      = user.interested_fields
    # eForm.tech_electives.data       = user.technical_electives
    
    if eForm.validate_on_submit():
        user.first_name            = eForm.first_name.data
        user.major                 = eForm.major.data
        user.gpa                   = eForm.cum_GPA.data
        user.graduation_data       = eForm.grad_date.data
        user.programming_languages = eForm.languages.data
       # user.research_experience   = eForm.prior_experience.data
        user.interested_fields     = eForm.research_topics.data
       # user.technical_electives   = eForm.tech_electives.data
        user.save_to_db()
        
        flash("Account information has been edited.")
        return redirect(url_for('routes.index'))
        
    return render_template('edit.html', form=eForm)
        
@bp_routes.route('/create_position', methods=['GET', 'POST'])
@login_required
def create_position():

    if not current_user.is_faculty():
        flash('Access Denied: not logged in as Faculty')
        return redirect(url_for('routes.index'))

    pform = CreatePositionForm()
    if pform.validate_on_submit():
        start_date  = datetime.strptime(pform.start_date.data, '%m/%d/%Y')
        end_date    = datetime.strptime(pform.end_date.data, '%m/%d/%Y')

        position = Position(title       = pform.title.data,
                            description = pform.description.data,
                            start_date  = start_date,
                            end_date    = end_date,
                            faculty_name= f'{current_user.first_name} {current_user.last_name}',
                            faculty_id  = current_user.id,
                            time_commitment          = int(pform.time_commitment.data),
                            required_qualifications  = pform.required_qualifications.data,
                            research_fields          = [x for x in pform.research_fields.data]
                            )

        position.save_to_db()
        flash('Position successfully created.')
        return redirect(url_for('routes.index'))

    return render_template('create.html', form=pform)
