from datetime import datetime
from flask_wtf import FlaskForm
from app.Model.experience_models import ProgrammingLanguage, TechnicalElective
from app.Model.position_models import ResearchField, Application
from app.Model import user_models
from wtforms.validators import ValidationError
from wtforms.widgets import CheckboxInput, ListWidget
import phonenumbers as phone

from flask_login import current_user

import wtforms
import wtforms.validators as validators
import wtforms_sqlalchemy.fields as fields

# TODO: Major as a table
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
    major = wtforms.StringField('Major', validators=[validators.DataRequired()])
    grad_dat = wtforms.DateField('Graduation Date', format='%Y-%m-%d', validators=[validators.DataRequired()])
    cum_GPA = wtforms.FloatField('Cumulative GPA', validators=[validators.DataRequired(), validators.NumberRange(min=0.0, max=5.0)])

    programming_languages = fields.QuerySelectMultipleField('Programming Languages',
                                                            query_factory=lambda: ProgrammingLanguage.query.all(),
                                                            get_label=lambda x: x.language,
                                                            widget=ListWidget(prefix_label=False),
                                                            option_widget=CheckboxInput()
                                                            )

    technical_electives = fields.QuerySelectMultipleField('Technical Electives',
                                                            query_factory=lambda: TechnicalElective.query.all(),
                                                            get_label=lambda x: x.course_title,
                                                            widget=ListWidget(prefix_label=False),
                                                            option_widget=CheckboxInput()
                                                            )
    
    
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = user_models.User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists. Please choose a different username.')
    
    def validate_wsu_id(self, wsu_id):
        if wsu_id.data != current_user.wsu_id:
            user = user_models.User.query.filter_by(wsu_id=wsu_id.data).first()
            if user:
                raise ValidationError('WSU ID already exists. Please choose a different WSU ID.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = user_models.User.query.filter_by(email=email.data).first()


    submit = wtforms.SubmitField('Submit')


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
        if user is not None and current_user.phone_number != field.data:
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