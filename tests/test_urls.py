import pytest

from app import create_app, db
from config import Config

import app.Model.position_models as position_models
import app.Model.user_models as user_models
import app.Model.experience_models as experience_models

S = user_models.Student
F = user_models.Faculty

# Response Codes
STATUS_CODE_SUCCESS = 200


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'bad-bad-key'
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True


def init_fields():

    
    if not position_models.ResearchField.query.count():
        fields = [
            'Electronic Design Automation (EDA)',           'High Performance Computing & Scalable Data Science',
            'Artificial Intelligence & Machine Learning',   'Bioinfomatics',
            'Distributed & Networked Systems',              'Power Engineering',
            'Systems Engineering',                          'Software Engineering'
            ]

        for field in fields:
            db.session.add(position_models.ResearchField(name=field))
        db.session.commit()


def init_languages():

    if not experience_models.ProgrammingLanguage.query.count():

        languages = [
            'C/C++', 'C#', '.NET', 'Haskell', 'Java', 'JavaScript', 'PowerShell', 'Python',
            'Pearl', 'SQL', 'R', 'Ruby', 'Rust', 'Swift', 'SystemVerilog', 'TeX', 'VHDL',
            'PHP', 'Objective-C', 'MatLab', 'Assembly', 'Go'
            ]
        languages = sorted(languages)

        for language in languages:
            db.session.add(experience_models.ProgrammingLanguage(language=language))
        db.session.commit()


def init_statuses():

    if not position_models.Status.query.count():
        statuses = ['Pending', 'Interview', 'Accepted', 'Rejected']
        for status in statuses:
            db.session.add(position_models.Status(status=status))
        db.session.commit()


def init_all():
    init_fields()
    init_languages()
    init_statuses()


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(config_class=TestConfig)
    db.init_app(flask_app)
    testing_client = flask_app.test_client()
    context = flask_app.app_context()
    context.push()
    yield testing_client
    context.pop()


@pytest.fixture
def init_database():
    db.create_all()
    init_all()

    s1 = S()
    s1.username = 'Student123'
    s1.email = 'student123@wsu.edu'
    s1.major = 'Computer Science'
    s1.first_name = 'John'
    s1.last_name = 'Doe'
    s1.set_password('123')
    s1.phone_number = '5098823444'
    s1.wsu_id = 915334469
    s1.gpa = 3.5
    s1.save_to_db()

    f1 = F()
    f1.first_name = 'Dr. Jane'
    f1.last_name = 'Foster'
    f1.email = 'janefoster@wsu.edu'
    f1.phone_number = '4429876543'
    f1.username = 'Faculty123'
    f1.set_password('123')
    f1.wsu_id = 915443123
    f1.save_to_db()

    yield

    db.drop_all()


def test_register_page(test_client):
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is requested (GET)
    THEN check that the response is valid
    '''
    response = test_client.get('/register')
    assert response.status_code == STATUS_CODE_SUCCESS
    assert b'Register' in response.data


def test_register(test_client, init_database):
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    '''
    response = test_client.post('/register',
                                data=dict(first_name='John',
                                    last_name='Doe',
                                    email='john.doe@gmail.com',
                                    phone_number='5322018899',
                                    username='johndoe',
                                    password1='123',
                                    password2='123',
                                    wsu_id=91533467),
                                follow_redirects=True
                                )
    assert response.status_code == STATUS_CODE_SUCCESS
    assert b'Cougar Research Application Portal' in response.data


def test_invalid_login(test_client, init_database):
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with correct credentials
    THEN check that the response is valid and login is successful
    '''
    response = test_client.post('/login',
                                data=dict(username='InvalidUser',
                                    password='123',
                                    remember_me=False),
                                follow_redirects=True
                                )
    assert response.status_code == STATUS_CODE_SUCCESS
    assert b'Invalid username or password' in response.data
    assert b'Sign In' in response.data
    assert b'Click to Create Account' in response.data


def test_login_logout():
    pass
