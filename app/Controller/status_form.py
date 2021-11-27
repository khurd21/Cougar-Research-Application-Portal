# status_forms.py
# Contains forms to update a student's status for an applied position

from flask_wtf import FlaskForm
import wtforms_sqlalchemy.fields as fields
import app.Model.position_models as position_models
import wtforms

class UpdateStatusForm(FlaskForm):

    statuses = fields.QuerySelectField('Status',
                                query_factory = lambda: position_models.Status.query.all(),
                                get_label     = lambda x: x.status
                                )
    submit = wtforms.SubmitField('Update Status')