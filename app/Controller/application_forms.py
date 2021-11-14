from datetime import datetime
from flask_wtf import FlaskForm
from app.Model.position_models import ResearchField
from wtforms.validators import ValidationError
from wtforms.widgets import CheckboxInput, ListWidget

import wtforms
import wtforms.validators as validators
import wtforms_sqlalchemy.fields as fields

class ApplicationForm(FlaskForm):
    reason          = wtforms.TextAreaField('Reason for Applying', validators=[validators.DataRequired()])
    ref_name        = wtforms.StringField('Faculty Reference Name', validators=[validators.DataRequired()])
    ref_email       = wtforms.StringField('Faculty Reference Email', validators=[validators.DataRequired(), validators.Email()])
    submit          = wtforms.SubmitField('Submit')
    