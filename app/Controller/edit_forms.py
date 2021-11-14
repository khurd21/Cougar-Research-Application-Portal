from datetime import datetime
from flask_wtf import FlaskForm
from app.Model.position_models import ResearchField
from app.Model import user_models
from wtforms.validators import ValidationError
from wtforms.widgets import CheckboxInput, ListWidget
import phonenumbers as phone

import wtforms
import wtforms.validators as validators
import wtforms_sqlalchemy.fields as fields

required = validators.DataRequired()
class EditForm(FlaskForm):
    username            = wtforms.StringField('Username',   validators=[validators.DataRequired()])
    wsu_id              = wtforms.StringField('WSU ID',     validators=[validators.DataRequired(), validators.Length(max=10)])
    first_name          = wtforms.StringField('First Name', validators=[validators.DataRequired()])
    last_name           = wtforms.StringField('Last Name',  validators=[validators.DataRequired()])
    email               = wtforms.StringField('Email',      validators=[validators.DataRequired(), validators.Email()])
    phone_number        = wtforms.StringField('Phone No.',  validators=[validators.DataRequired()])
    password1           = wtforms.PasswordField('Password', validators=[validators.DataRequired()])
    password2           = wtforms.PasswordField('Re-enter Password', validators=[validators.DataRequired(), validators.EqualTo('password1')])
    major               = wtforms.SelectField('Major', validators=[required])
    cum_GPA             = wtforms.FloatField('Cumulative GPA', validators=[required])
    grad_date           = wtforms.StringField('Graduation Date [mm/dd/yyyy]', validators=[required])
    tech_electives      = wtforms.SelectMultipleField('Technical Electives', validators=[required])
    research_topics     = wtforms.SelectMultipleField('Research Topics of Interest', validators=[required])
    languages           = wtforms.StringField('Programming Languages (separate each language by a semi-colon)', validators=[required])
    prior_experience    = wtforms.TextAreaField('Prior Research Experience', validators=[required])
    submit              = wtforms.SubmitField('Submit Changes')
    
    def validate_username(self, field):
        user = user_models.User.query.filter_by(username=field.data).first()
        if user is not None:
            raise ValidationError('Username already in use by another account.')


    def validate_wsu_id(self, field):
        user = user_models.User.query.filter_by(wsu_id=int(field.data)).first()
        if user is not None:
            raise ValidationError('WSU ID already in use by another account.')


    def validate_email(self, field):
        user = user_models.User.query.filter_by(email=field.data).first()
        if user is not None:
            raise ValidationError('Email already in use by another account.')


    def validate_phone_number(self, field):
        
        user = user_models.User.query.filter_by(phone_number=field.data).first()
        if user is not None:
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