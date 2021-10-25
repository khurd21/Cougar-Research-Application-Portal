# edit_forms.py
# Contains forms to edit user info

from datetime import datetime
from flask_wtf import FlaskForm
from app.Model.position_models import ResearchField
from wtforms.validators import ValidationError


import wtforms
import wtforms.validators as validators
import wtforms_sqlalchemy.fields as fields



class CreatePositionForm(FlaskForm):

    title           = wtforms.StringField('Position Title',             validators=[validators.DataRequired()])
    description     = wtforms.TextAreaField('Description of Position',  validators=[validators.DataRequired()])
    required_qualifications = wtforms.TextAreaField('Required Qualifications', validators=[validators.DataRequired()])
    start_date      = wtforms.StringField('Start Date [mm/dd/yyyy] (leave empty for current date)',validators=[validators.DataRequired()])
    end_date        = wtforms.StringField('End Date [mm/dd/yyyy]',      validators=[validators.DataRequired()])
    time_commitment = wtforms.StringField('Hours per Week',             validators=[validators.DataRequired()])

    research_fields = fields.QuerySelectMultipleField('Research Fields',
                                            query_factory   = lambda  : ResearchField.query.all(),
                                            get_label       = lambda x: x.name
                                            )
    start_date_helper = datetime.utcnow()


    def validate_start_date(self, field):
        try:
           date = datetime.strptime(field.data, '%m/%d/%Y')
        except ValueError:
            raise ValidationError('Make sure date format is: [mm/dd/yyyy]')

        self.start_date_helper = date


    def validate_end_date(self, field):
        try:
            date = datetime.strptime(field.data, '%m/%d/%Y')
        except ValueError:
            raise ValidationError('Make sure date format is: [mm/dd/yyyy]')
        if date < self.start_date_helper:
            raise ValidationError('End date must exceed start date.')


    def validate_time_commitment(self, field):
        try:
            value = int(field.data)
        except ValueError:
            raise ValidationError('Time commitment must be an integer (hours per week)')
