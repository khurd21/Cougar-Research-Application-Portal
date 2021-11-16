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
    username            = wtforms.StringField('Username',   validators=[validators.DataRequired()])
    wsu_id              = wtforms.StringField('WSU ID',     validators=[validators.DataRequired(), validators.Length(max=10)])
    first_name          = wtforms.StringField('First Name', validators=[validators.DataRequired()])
    last_name           = wtforms.StringField('Last Name',  validators=[validators.DataRequired()])
    email               = wtforms.StringField('Email',      validators=[validators.DataRequired(), validators.Email()])
    phone_number        = wtforms.StringField('Phone No.',  validators=[validators.DataRequired()])
    # TODO: major               = wtforms.SelectField('Major', choices=get_major_choices())
    major               = wtforms.StringField('Major', validators=[validators.DataRequired()])
    cum_GPA             = wtforms.FloatField('Cumulative GPA', validators=[validators.DataRequired()])
    grad_date           = wtforms.StringField('Graduation Date [mm/dd/yyyy]', validators=[validators.DataRequired()])

    # TODO: URGENT Move tech_electives to a table
    #tech_electives      = wtforms.SelectMultipleField('Technical Electives', query_factory=lambda: TechnicalElective.query.all(), get_label=lambda x: x.course_title,)
    #prior_experience    = wtforms.TextAreaField('Prior Research Experience', validators=[validators.DataRequired()])
    research_topics     = fields.QuerySelectMultipleField('Research Topics of Interest',
                                                        query_factory=lambda: ResearchField.query.all(),
                                                        get_label=lambda x: x.name,
                                                        widget=ListWidget(prefix_label=False),
                                                        option_widget=CheckboxInput()
                                                        )                                                 
    languages           = fields.QuerySelectMultipleField('Programming Languages', 
                                                        query_factory=lambda: ProgrammingLanguage.query.all(),
                                                        get_label=lambda x: x.language,
                                                        widget=ListWidget(prefix_label=False),
                                                        option_widget=CheckboxInput()
                                                        )
    submit              = wtforms.SubmitField('Submit Changes')
    

    def validate_username(self, field):
        user = user_models.User.query.filter_by(username=field.data).first()
        if user is not None and user.username != current_user.username:
            raise ValidationError('Username already in use by another account.')


    def validate_wsu_id(self, field):
        user = user_models.User.query.filter_by(wsu_id=int(field.data)).first()
        if user is not None and user.wsu_id != current_user.wsu_id:
            raise ValidationError('WSU ID already in use by another account.')


    def validate_email(self, field):
        user = user_models.User.query.filter_by(email=field.data).first()
        if user is not None and user.email != current_user.email:
            raise ValidationError('Email already in use by another account.')


    def validate_phone_number(self, field):
        
        user = user_models.User.query.filter_by(phone_number=field.data).first()
        if user is not None and user.phone_number != current_user.phone_number:
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


    def validate_grad_date(self, field):
        try:
            date = datetime.strptime(field.data, '%m/%d/%Y')
        except ValueError:
            raise ValidationError('Invalid date format.')


    def validate_cum_GPA(self, field):
        try:
            cum_GPA = float(field.data)
        except ValueError:
            raise ValidationError('Invalid GPA format. Make sure it is a real number.')

        if cum_GPA < 0 or cum_GPA > 5:
            raise ValidationError('Invalid GPA. GPA must be between 0 and 5.')