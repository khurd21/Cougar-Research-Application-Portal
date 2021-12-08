from threading import currentThread
from flask import Blueprint
from app.Model import position_models
from app.Model.experience_models import TechnicalElective, ResearchExperience
from config import Config
from flask_login import current_user, login_required
from app.Model.position_models import Position, Application
from app.Model.user_models import User
from flask import render_template, flash, redirect, url_for, request
from app import db
from flask_login import current_user, login_user, logout_user, login_required
from app.Controller.position_forms import CreatePositionForm, SortForm
from app.Controller.application_forms import ApplicationForm
from app.Controller.edit_forms import EditTechnicalElectiveForm, EditResearchExperienceForm, EditPositionForm, FacultyEditForm, StudentEditForm

import app.Model.user_models as user_models
import app.Model.experience_models as experience_models
import app.Controller.status_form as status_form
from datetime import datetime

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'
bp_routes.static_folder = Config.STATIC_FOLDER

recentSort = ''

## FUTURE: With faculty, sort so faculty id is on top? Or only show faculty's post?
@bp_routes.route('/', methods=['GET', 'POST'])
@bp_routes.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    sForm = SortForm()
    positions = []
    
    if not current_user.is_faculty():
        for deleted_pos in current_user.deleted_positions:
            flash(f'"{deleted_pos.position_title}" has been deleted. Last status: {deleted_pos.last_status}')
            db.session.delete(deleted_pos)
            db.session.commit()
        if sForm.validate_on_submit():
            choice = sForm.sort_choice.data
            positions = eval(choice)
        else:
            positions = Position.query.all()   
        current_user.deleted_positions.clear() 
        db.session.commit()
    else:
        positions = Position.query.all()

    return render_template('index.html', research_positions=positions, form=sForm)

def get_recommended_positions():
    display_positions = []
    positions = Position.query.all()
    for p in positions:
        fields = p.research_fields
        for field in current_user.interested_fields:
            if fields.count(field) > 0:
                display_positions.append(p)
                break
            
    return display_positions

@bp_routes.route('/position/<pos_id>', methods=['GET'])
@login_required
def display_position(pos_id):
    position = Position.query.filter_by(id=int(pos_id)).first()
    user = User.query.filter_by(id=position.faculty_id).first()
    return render_template('position.html', position=position, user=user)


@bp_routes.route('/view_applied_positions', methods=['GET'])
@login_required
def view_applied_positions():
    if current_user.is_faculty():
        flash('Access Denied: not logged in as Student')
        return redirect(url_for('routes.index'))
    
    return render_template('student_positions.html', positions=current_user.applied_positions)


@bp_routes.route('/view_applicants', methods=['GET'])
@login_required
def view_applicants():
    if not current_user.is_faculty():
        flash('Access Denied: not logged in as Faculty')
        return redirect(url_for('routes.index'))
    
    positions = current_user.posted_positions
    return render_template('faculty_positions.html', positions=positions)


@bp_routes.route('/student/<student_id>/<pos_id>', methods=['GET', 'POST'])
@login_required
def display_applicant_info(student_id, pos_id):
    if not current_user.is_faculty():
        flash('Access Denied: not logged in as Faculty')
        return redirect(url_for('routes.index'))
    
    student = User.query.filter_by(id=int(student_id)).first()
    position = Position.query.filter_by(id=int(pos_id)).first()
    application = Application.query.filter_by(student_id=student.id).filter_by(position_id=position.id).first()

    if application is None:
        flash('Application does not exist.')
        return redirect(url_for('routes.view_applicants'))

    status = position_models.Status.query.filter_by(id=int(application.status_id)).first()

    form = status_form.UpdateStatusForm()
    if form.validate_on_submit():
        application.status_id = form.statuses.data.id
        status = position_models.Status.query.filter_by(id=int(form.statuses.data.id)).first()
        flash(f'Status Updated: {status.status}')
        db.session.commit()

    return render_template('applicant_info.html',
            student=student, position=position,
            application=application, form=form,
            status=status
            )


@bp_routes.route('/apply/<pos_id>', methods=['GET', 'POST'])
@login_required
def apply(pos_id):
    if current_user.is_faculty():
        flash('Access Denied: You must be logged in as a student to apply for a position.')
        return redirect(url_for('routes.index'))

    position = Position.query.filter_by(id=int(pos_id)).first()
    if position is None:
        flash('Position not found')
        return redirect(url_for('routes.index'))
    faculty = user_models.User.query.filter_by(id=position.faculty_id).first()
    
    application = Application.query.filter_by(position_id=int(pos_id), student_id=current_user.id).first() 
    if application is not None:
        flash(f'You have already applied for this position: {position.title}')
        return redirect(url_for('routes.index'))


    appForm = ApplicationForm()
    if appForm.validate_on_submit():
        pending     = position_models.Status.query.filter_by(status='Pending').first()
        application = Application(description=appForm.description.data, ref_name=appForm.ref_name.data,
                                    ref_email=appForm.ref_email.data, position_id=pos_id,
                                    student_id=current_user.id, status_id=pending.id,
                                    )
        application.save_to_db()
        current_user.application_forms.append(application)
        current_user.applied_positions.append(position)
        position.application_forms.append(application)
        db.session.commit()
        flash('Application successfully submitted.')
        return redirect(url_for('routes.index'))
    
    return render_template('apply.html', form=appForm, pos_id=pos_id, position=position, user=faculty)


@bp_routes.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    user = User.query.filter_by(id=current_user.id).first()

    if user is None:
        flash('User could not be found to edit')
        return redirect(url_for('routes.index'))
    
    if current_user.is_faculty():
        eForm = FacultyEditForm(obj=user)
    else:
        eForm = StudentEditForm(obj=user)
    
    if eForm.validate_on_submit():
        eForm.populate_obj(user)
        db.session.commit()
        
        flash("Account information has been edited.")
        return redirect(url_for('routes.index'))
        
    return render_template('edit.html', form=eForm)

@bp_routes.route('/technical_electives', methods=['GET'])
@login_required
def technical_electives():
    if current_user.is_faculty():
        flash('Access Denied: You must be logged in as a student to apply for a position.')
        return redirect(url_for('routes.index'))

    technical_electives = current_user.technical_electives
    return render_template('tech_electives.html', electives=technical_electives)


@bp_routes.route('/create_technical_elective', methods=['GET', 'POST'])
@login_required
def create_technical_elective():

    if current_user.is_faculty():
        flash('Access Denied: You must be logged in as a student to apply for a position.')
        return redirect(url_for('routes.index'))


    form = EditTechnicalElectiveForm()
    if form.validate_on_submit():
        technical_elective = TechnicalElective(course_num=form.course_num.data, course_title=form.course_title.data,
                                                course_prefix=form.course_prefix.data, course_description=form.course_description.data,
                                                student_id=current_user.id, grade_id=form.grade_id.data.id
                                                )
        technical_elective.save_to_db()
        current_user.technical_electives.append(technical_elective)
        db.session.commit()
        flash("Technical Elective successfully added.")
        return redirect(url_for('routes.technical_electives'))
    
    return render_template('create_tech_elective.html', form=form)


@bp_routes.route('/research_experience', methods=['GET'])
@login_required
def research_experience():

    if current_user.is_faculty():
        flash('Access Denied: You must be logged in as a student to apply for a position.')
        return redirect(url_for('routes.index'))

    research_experience = current_user.research_experience 
    return render_template('prior_experiences.html', experiences=research_experience)


@bp_routes.route('/create_research_experience', methods=['GET', 'POST'])
@login_required
def create_research_experience():
    if current_user.is_faculty():
        flash('Access Denied: You must be logged in as a student to apply for a position.')
        return redirect(url_for('routes.index'))
    
    form = EditResearchExperienceForm()
    if form.validate_on_submit():

        research_experience = ResearchExperience(student_id=current_user.id, title=form.title.data,
                                                    company=form.company.data, description=form.description.data,
                                                    start_date=form.start_date.data, end_date=form.end_date.data)
        research_experience.save_to_db()
        current_user.research_experience.append(research_experience)
        db.session.commit()
        flash('Research Experience succesfully added.')
        return redirect(url_for('routes.research_experience'))
    
    return render_template('create_prior_experience.html', form=form)



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
                            faculty_id  = current_user.id,
                            time_commitment          = int(pform.time_commitment.data),
                            required_qualifications  = pform.required_qualifications.data,
                            research_fields          = [x for x in pform.research_fields.data]
                            )

        position.save_to_db()
        current_user.posted_positions.append(position)
        db.session.commit()
        flash('Position successfully created.')
        return redirect(url_for('routes.index'))

    return render_template('create.html', form=pform)

@bp_routes.route('/edit_position/<pos_id>', methods=['GET', 'POST'])
@login_required
def edit_position(pos_id):

    post = Position.query.filter_by(id=int(pos_id)).first()

    if post is None:
        flash('Position not found.')
        return redirect(url_for('routes.index'))
        
    if current_user.id != post.faculty_id:
        flash('Access Denied: You must be logged in as this position\'s faculty member to edit it.')
        return redirect(url_for('routes.index'))

    eForm = EditPositionForm(obj=post)
    
    if eForm.validate_on_submit():
        eForm.populate_obj(post)
        db.session.commit()
        
        flash("Position information has been edited.")
        return redirect(url_for('routes.index'))
        
    return render_template('edit_position.html', form=eForm)

@bp_routes.route('/delete_position/<pos_id>', methods=['POST', 'DELETE', 'GET'])
@login_required
def delete_position(pos_id):
    
    if not current_user.is_faculty():
        flash('Access Denied: not logged in as faculty.')
        return redirect(url_for('routes.position', id=pos_id))
    
    position = Position.query.filter_by(id=pos_id).first()
    if not position in current_user.posted_positions:
        flash('Access Denied: you are not the owner of this position.')
        return redirect(url_for('routes.position', id=pos_id))

    for applicant in position.application_forms:

        status = position_models.Status.query.filter_by(id=applicant.status_id).first()
        student = user_models.User.query.filter_by(id=applicant.student_id).first()

        if student:
            deleted_pos = position_models.DeletedPosition(student_id=student.id, position_title=position.title, last_status=status.status)
            deleted_pos.save_to_db()
            student.deleted_positions.append(deleted_pos)
            db.session.commit()
            student.save_to_db()

        db.session.delete(applicant)

    position.students.clear()
    position.application_forms.clear()
    position.research_fields.clear()

    db.session.delete(position)
    db.session.commit()

    flash('Post deleted.')
    return redirect(url_for('routes.index'))


@bp_routes.route('/delete_application/<app_id>', methods=['POST','DELETE'])
@login_required
def delete_application(app_id):
    
    if current_user.is_faculty():
        flash('Access Denied: Faculty cannot delete a student application.')
        return redirect(url_for('routes.index'))
    
    application = Application.query.filter_by(id=int(app_id)).filter_by(student_id=current_user.id).first()
    if not application:
        flash('Access Denied: Student does not have access to this application.')
        return redirect(url_for('routes.index'))
   

    position = position_models.Position.query.filter_by(id=application.position_id).first()
    status   = position_models.Status.query.filter_by(id=application.status_id).first()
    faculty  = user_models.Faculty.query.filter_by(id=position.faculty_id).first()

    current_user.applied_positions.remove(position)
    current_user.application_forms.remove(application)
    position.application_forms.remove(application)

    db.session.delete(application)
    db.session.commit()

    flash('Application deleted.')
    return redirect(url_for('routes.view_applied_positions'))


@bp_routes.route('/delete_prior_experience/<exp_id>', methods=['POST', 'DELETE'])
@login_required
def delete_prior_experience(exp_id):
    
    if current_user.is_faculty():
        flash('Access Denied: Must be logged in as student')
        return redirect(url_for('routes.index'))

    prior_experience = experience_models.ResearchExperience.query.filter_by(id=exp_id).first()
    if not prior_experience in current_user.research_experience:
        flash('Access Denied: You don\'t have permission to modify this research experience.')
        return redirect(url_for('routes.research_experience'))

    current_user.research_experience.remove(prior_experience)
    db.session.delete(prior_experience)
    db.session.commit()
    flash(f'Research Experience Deleted: {prior_experience.title}')
    return redirect(url_for('routes.research_experience'))


@bp_routes.route('/delete_technical_elective/<tech_id>', methods=['POST', 'DELETE'])
@login_required
def delete_technical_elective(tech_id):

    if current_user.is_faculty():
        flash('Access Denied: Must be logged in as a student')
        return redirect(url_for('routes.index'))

    technical_elective = experience_models.TechnicalElective.query.filter_by(id=tech_id).first()
    if not technical_elective in current_user.technical_electives:
        flash('Access Denied: You dont\'t have permission to modify this technical elective.')
        return redirect(url_for('routes.technical_electives'))

    current_user.technical_electives.remove(technical_elective)
    db.session.delete(technical_elective)
    db.session.commit()
    flash(f'Technical Elective Deleted: {technical_elective.course_title}')
    return redirect(url_for('routes.technical_electives'))


@bp_routes.route('/edit_research_experience/<rexp_id>', methods=['GET', 'POST'])
@login_required
def edit_research_experience(rexp_id):

    experience = ResearchExperience.query.filter_by(id=int(rexp_id)).first()

    if experience is None:
        flash('Research Experience not found.')
        return redirect(url_for('routes.index'))
        
    if current_user.id != experience.student_id:
        flash('Access Denied: You must be logged in as this Research Experience\'s student user to edit it.')
        return redirect(url_for('routes.index'))

    eForm = EditResearchExperienceForm(obj=experience)
    
    if eForm.validate_on_submit():
        eForm.populate_obj(experience)
        db.session.commit()
        
        flash("Research Experience information has been edited.")
        return redirect(url_for('routes.research_experience'))
        
    return render_template('edit_research_experience.html', form=eForm)


@bp_routes.route('/edit_technical_elective/<elect_id>', methods=['GET', 'POST'])
@login_required
def edit_technical_elective(elect_id):

    elective = TechnicalElective.query.filter_by(id=int(elect_id)).first()

    if elective is None: 
        flash('Technical Elective not found.')
        return redirect(url_for('routes.index'))
        
    if current_user.id != elective.student_id:
        flash('Access Denied: You must be logged in as this Technical Elective\'s student user to edit it.')
        return redirect(url_for('routes.index'))

    eForm = EditTechnicalElectiveForm(obj=elective)
    
    if eForm.validate_on_submit():
        eForm.populate_obj(elective)
        elective.grade_id = eForm.grade_id.data.id
        db.session.commit()
        
        flash("Technical Elective information has been edited.")
        return redirect(url_for('routes.technical_electives'))
        
    return render_template('edit_tech_elective.html', form=eForm)
