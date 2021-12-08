from datetime import datetime
from flask_wtf import FlaskForm
from app.Model.experience_models import ProgrammingLanguage, ResearchExperience, TechnicalElective
from app.Model.position_models import ResearchField, Application
from app.Model import user_models
from wtforms.validators import ValidationError
from wtforms.widgets import CheckboxInput, ListWidget
import phonenumbers as phone
 
from flask_login import current_user

import wtforms
import wtforms.validators as validators
import wtforms_sqlalchemy.fields as fields


def get_major_choices():
    majors = user_models.Major.query.all()
    tuple_majors = [(major.id, major.name) for major in majors]
    return tuple_majors

class EditForm(FlaskForm):
    username = wtforms.StringField('Username', validators=[validators.DataRequired()])
    wsu_id = wtforms.StringField('WSU ID', validators=[validators.DataRequired(), validators.Length(max=10)])
    first_name = wtforms.StringField('First Name', validators=[validators.DataRequired()])
    last_name = wtforms.StringField('Last Name', validators=[validators.DataRequired()])
    email = wtforms.StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    phone_number = wtforms.StringField('Phone No.', validators=[validators.DataRequired()])


    def validate_username(self, field):
        user = user_models.User.query.filter_by(username=field.data).first()
        print(f'CURRENT USER: {current_user.username} FIELD DATA: {field.data}')
        if user is not None and current_user.username != field.data:
            raise ValidationError('Username already in use.')


    def validate_wsu_id(self, field):
        user = user_models.User.query.filter_by(wsu_id=int(field.data)).first()
        if user is not None and current_user.wsu_id != int(field.data):
            raise ValidationError('WSU ID already in use.')


    def validate_email(self, field):
        user = user_models.User.query.filter_by(email=field.data).first()
        if user is not None and current_user.email != field.data:
            raise ValidationError('Email already in use.')


    def validate_phone_number(self, field):
        
        user = user_models.User.query.filter_by(phone_number=field.data).first()
        if user is not None and str(current_user.phone_number) != str(field.data):
            raise ValidationError('Phone number already in use by another account.')

        if len(field.data) > 16:
            raise ValidationError('Invalid phone number')

        try:
            input_number = phone.parse(field.data)
            if not (phone.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')

        except:
            input_number = phone.parse("+1"+field.data)
            if not (phone.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
    

class FacultyEditForm(EditForm):

    submit = wtforms.SubmitField('Submit')


class StudentEditForm(EditForm):

    major = wtforms.StringField('Major', validators=[validators.DataRequired()])
    graduation_date = wtforms.DateField('Graduation Date [mm/dd/yyyy]', format='%m/%d/%Y', validators=[validators.DataRequired()])
    gpa = wtforms.FloatField('Cumulative GPA', validators=[validators.DataRequired(), validators.NumberRange(min=0.0, max=5.0)])

    programming_languages = fields.QuerySelectMultipleField('Programming Languages',
                                                            query_factory=lambda: ProgrammingLanguage.query.all(),
                                                            get_label=lambda x: x.language,
                                                            widget=ListWidget(prefix_label=False),
                                                            option_widget=CheckboxInput()
                                                            )

    interested_fields = fields.QuerySelectMultipleField('Research Topics',
                                                            query_factory=lambda: ResearchField.query.all(),
                                                            get_label=lambda x: x.name,
                                                            widget=ListWidget(prefix_label=False),
                                                            option_widget=CheckboxInput()
                                                            )


    submit = wtforms.SubmitField('Submit')

class EditPositionForm(FlaskForm):
    
    title = wtforms.StringField('Title', validators=[validators.DataRequired(), validators.Length(max=32)])
    description = wtforms.TextAreaField('Description', validators=[validators.DataRequired(), validators.Length(max=1000)])
    start_date = wtforms.DateTimeField('Start Date [mm/dd/yyyy]', format='%m/%d/%Y', validators=[validators.DataRequired()])
    end_date = wtforms.DateTimeField('End Date [mm/dd/yyyy]', format='%m/%d/%Y', validators=[validators.DataRequired()])
    time_commitment = wtforms.IntegerField('Time Commitment', validators=[validators.DataRequired(), validators.NumberRange(min=1,max=100)])
    required_qualifications = wtforms.TextAreaField('Required Qualifications', validators=[validators.DataRequired(), validators.Length(max=512)])

    research_fields = fields.QuerySelectMultipleField('Research Fields',
                                                            query_factory=lambda: ResearchField.query.all(),
                                                            get_label=lambda x: x.name,
                                                            widget=ListWidget(prefix_label=False),
                                                            option_widget=CheckboxInput()
                                                            )
    
    submit = wtforms.SubmitField('Submit')

    def validate_end_date(self, field):
        if field.data < self.start_date.data:
            raise ValidationError('End date must be after start date.')

class EditTechnicalElectiveForm(FlaskForm):

    course_prefix      = wtforms.StringField('Course Prefix', validators=[validators.DataRequired(), validators.Length(max=8)])
    course_num         = wtforms.IntegerField('Course Number', validators=[validators.DataRequired()])
    course_title       = wtforms.StringField('Course Title', validators=[validators.DataRequired(), validators.Length(max=32)])
    course_description = wtforms.TextAreaField('Course Description', validators=[validators.DataRequired(), validators.Length(max=512)])

    submit = wtforms.SubmitField('Submit')

class EditResearchExperienceForm(FlaskForm):

    title        = wtforms.StringField('Title', validators=[validators.DataRequired(), validators.Length(max=64)])
    company      = wtforms.StringField('Organization', validators=[validators.DataRequired(), validators.Length(max=32)])
    description  = wtforms.TextAreaField('Description', validators=[validators.DataRequired(), validators.Length(max=512)])
    start_date   = wtforms.DateTimeField('Start Date [mm/dd/yyyy]', format='%m/%d/%Y', validators=[validators.DataRequired()])
    end_date     = wtforms.DateTimeField('End Date [mm/dd/yyyy]', format='%m/%d/%Y', validators=[validators.DataRequired()])

    submit = wtforms.SubmitField('Submit')

    def validate_end_date(self, field):
        if field.data < self.start_date.data:
            raise ValidationError('End date must be after start date.')
