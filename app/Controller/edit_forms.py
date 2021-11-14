from datetime import datetime
from flask_wtf import FlaskForm
from app.Model.position_models import ResearchField
from wtforms.validators import ValidationError
from wtforms.widgets import CheckboxInput, ListWidget

import wtforms
import wtforms.validators as validators
import wtforms_sqlalchemy.fields as fields

class EditForm(FlaskForm):
    first_name          = wtforms.StringField('First Name')
    major               = wtforms.SelectField('Major')
    cum_GPA             = wtforms.FloatField('Cumulative GPA')
    grad_date           = wtforms.StringField('Graduation Date [mm/dd/yyyy]')
    tech_electives      = wtforms.SelectMultipleField('Technical Electives')
    research_topics     = wtforms.SelectMultipleField('Research Topics of Interest')
    languages           = wtforms.StringField('Programming Languages (separate each language by a semi-colon)')
    prior_experience    = wtforms.TextAreaField('Prior Research Experience')
    submit              = wtforms.SubmitField('Submit Changes')