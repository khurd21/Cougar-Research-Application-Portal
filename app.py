
from app import create_app, db
from app.Model import position_models
from datetime import datetime
from flask_login import current_user


from app.Model.position_models import ResearchField, Position
from app.Model.user_models import User, Faculty, Student

app = create_app()

@app.before_first_request
def init_db(*args, **kwargs):
    db.create_all()
    if position_models.ResearchField.query.count() == 0:
        fields = [
                'Electronic Design Automation (EDA)',           'High Performance Computing & Scalable Data Science',
                'Artificial Intelligence & Machine Learning',   'Bioinfomatics',
                'Distributed & Networked Systems',              'Power Engineering',
                'Systems Engineering',                          'Software Engineering'
                ]

        for field in fields:
            db.session.add(position_models.ResearchField(name=field))
        db.session.commit()

    if position_models.Status.query.count() == 0:
        statuses = ['Pending', 'Interview', 'Accepted', 'Rejected']
        for status in statuses:
            db.session.add(position_models.Status(status=status))
        db.session.commit()
    
    return None

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.add(current_user)
        db.session.commit()


if __name__ == '__main__':
    app.run()
