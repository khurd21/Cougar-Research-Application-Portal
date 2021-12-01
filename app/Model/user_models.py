# user_models.py
# Contains the User models 

from app import login, db
from app.Model import position_models, tables, experience_models

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


@login.user_loader
def user_loader(id):
    return User.query.filter_by(id = int(id)).first()


### User Models ###

class User(db.Model, UserMixin):
    '''
    Base class for the User Account Model. Contains the base data for all type User.

    :param Model SQLAlchemy: The model database
    :param UserMixin Inherited Class: Provides the default implementations expected by Flask-Login

    :value id db.Integer: Unique id for user
    :value username db.String: Unique username for user
    :value email db.String: Unique email for user
    :value passwd_hash db.String: Encrypted password for user
    '''

    __tablename__ = 'user'

    type        = db.Column(db.String(64))
    id          = db.Column(db.Integer, primary_key=True)

    first_name  = db.Column(db.String(32))
    last_name   = db.Column(db.String(32))
    wsu_id      = db.Column(db.Integer)
    username    = db.Column(db.String(32), unique=True)
    email       = db.Column(db.String(64), unique=True)
    phone_number= db.Column(db.Integer, unique=True)
    last_seen   = db.Column(db.DateTime, default=datetime.utcnow)

    passwd_hash = db.Column(db.String(128))


    __mapper_args__ = {
            'polymorphic_identity': 'user',
            'polymorphic_on':type
            }



    def set_password(self, passwrd):
        self.passwd_hash = generate_password_hash(passwrd)


    def check_password(self, passwrd):
        return check_password_hash(self.passwd_hash, passwrd)


    def is_faculty(self):
        return type(self) == Faculty


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def __repr__(self):
        return f'<User id: {self.id} username: {self.username} email: {self.email}>'




class Faculty(User):

    posted_positions = db.relationship('Position', backref='faculty_info', lazy=True)
    deleted_applications = db.relationship('DeletedApplication', lazy=True)

    __mapper_args__ = {
            'polymorphic_identity': 'faculty'
            }



# For accessing research experience, technical electives, only add them to the Student Model!
class Student(User):

    major                       = db.Column(db.String(32))   
    graduation_date             = db.Column(db.DateTime,default=datetime.utcnow)
    gpa                         = db.Column(db.Float)
    technical_electives         = db.relationship('TechnicalElective', backref='student', lazy=True)
    research_experience         = db.relationship('ResearchExperience', lazy=True)
    application_forms           = db.relationship('Application', lazy=True)
    deleted_positions           = db.relationship('DeletedPosition', lazy=True)


    programming_languages = db.relationship('ProgrammingLanguage',
                                        secondary=tables.programming_languages, lazy='subquery',
                                        back_populates='students')

    applied_positions = db.relationship('Position',
                                        secondary=tables.applied_positions, lazy='subquery',
                                        back_populates='students'
                                        )

    interested_fields = db.relationship('ResearchField',
                            secondary=tables.interested_fields, lazy='subquery',
                            back_populates='students'
                            )


    __mapper_args__ = {
            'polymorphic_identity': 'student'
            }

    def get_position_for_application(self, app_id):
        application = position_models.Application.query.filter_by(id=int(app_id)).first()
        if application in self.application_forms:
            return position_models.Position.query.filter_by(id=application.position_id).first()
        return None
