# user_models.py
# Contains the User models 

from app import db, login
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash



@login.user_loader
def user_loader(id):
    return User.query.get(int(id))


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
    username    = db.Column(db.String(32), unique=True)
    email       = db.Column(db.String(64), unique=True)
    passwd_hash = db.Column(db.String(128))


    # How we are able to use User for grabbing each polymorphic type
    # From database
    __mapper_args__ = {
            'polymorphic_identity': 'user',
            'polymorphic_on':type
            }


    def set_password(self, passwrd):
        self.passwd_hash = generate_password_hash(passwrd)


    def check_password(self, passwrd):
        return check_password_hash(self.passwd_hash, passwrd)


    def __repr__(self):
        return f'<User id: {self.id} username: {self.username} email: {self.email}>'





class Faculty(User):

    posted_positions = None # relationship to positions db
    # Others ??

    __mapper_args__ = {
            'polymorphic_identity': 'faculty'
            }



class Student(User):

    applied_positions = None # relationship to positions db
    # Others ??

    __mapper_args__ = {
            'polymorphic_identity': 'student'
            }

