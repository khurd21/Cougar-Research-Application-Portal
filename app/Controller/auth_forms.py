# forms.py
# 

from flask_wtf import FlaskForm
from flask_login import current_user

from app.Model import user_models, position_models
from wtforms.validators import ValidationError

import wtforms
import wtforms.validators as validators
import wtforms_sqlalchemy.fields as fields
import phonenumbers as phone



class RegisterForm(FlaskForm):

    username    = wtforms.StringField('Username',   validators=[validators.DataRequired()])
    wsu_id      = wtforms.StringField('WSU ID',     validators=[validators.DataRequired(), validators.Length(max=10)])
    first_name  = wtforms.StringField('First Name', validators=[validators.DataRequired()])
    last_name   = wtforms.StringField('Last Name',  validators=[validators.DataRequired()])
    email       = wtforms.StringField('Email',      validators=[validators.DataRequired(), validators.Email()])
    phone_number= wtforms.StringField('Phone No.',  validators=[validators.DataRequired()])

    password1   = wtforms.PasswordField('Password', validators=[validators.DataRequired()])
    password2   = wtforms.PasswordField('Re-enter Password', validators=[validators.DataRequired(), validators.EqualTo('password1')])

    is_faculty  = wtforms.BooleanField('Register as Faculty?')
    submit      = wtforms.SubmitField('Register')

    
    def validate_wsu_id(self, field):
        user = user_models.User.query.filter_by(wsu_id=int(field.data)).first()
        if user is not None:
            raise ValidationError('WSU ID already in use by another account.')


    def validate_username(self, field):
        user = user_models.User.query.filter_by(username=field.data)
        if user is not None:
            raise ValidationError('Username already in use by another account.')


    def validate_email(self, field):
        user = user_models.User.query.filter_by(email=field.data)
        if user is not None:
            raise ValidationError('Email already in use by another account..')


    def validate_phone_number(self, field):
        
        user = user_models.User.query.filter_by(phone_number=field.data)
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
            


class LoginForm(FlaskForm):

    username    = wtforms.StringField('Username')
    password    = wtforms.PasswordField('Password')
    remember_me = wtforms.BooleanField('Remember Me?')
    submit      = wtforms.SubmitField('Log In')
