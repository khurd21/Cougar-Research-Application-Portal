from operator import pos
import pytest

from app import create_app, db
from config import Config

import app.Model.position_models as position_models
from app.Model.user_models import Faculty
import app.Model.user_models as user_models
import app.Model.experience_models as experience_models
from datetime import datetime, timedelta

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
    
def create_student():
        return user_models.Student(username='test_student', email='test_email@test.com',
                                major='test_major', phone_number='1234567890',
                                first_name='test', last_name='student',
                                wsu_id=123456789, gpa=2.0)

def create_faculty():
    return user_models.Faculty(username='test_faculty', email='test_faculty@test.com',
                                    phone_number='1234567891', wsu_id=123446789,
                                    first_name='test', last_name='faculty'
                                    )

def create_position(faculty):
    return position_models.Position(title='test_position', description='test_description',
                                    faculty_name=f'{faculty.first_name} {faculty.last_name}', faculty_id=faculty.id,
                                    required_qualifications='test_qualifications', start_date=datetime.utcnow(),
                                    end_date=datetime.utcnow() + timedelta(days=1)
                                    )

def create_application(student, position):
    return position_models.Application(student_id=student.id, position_id=position.id,
                                        description='test_description', student_name=f'{student.first_name} {student.last_name}',
                                        ref_name='test_ref_name', ref_email='test_ref_email'
                                        )

def create_position(fields):
    p1 = position_models.Position(faculty_id = f1.id)   
    p1.start_date = datetime.utcnow()
    p1.end_date = datetime.utcnow() + timedelta(days=30)
    p1.required_qualifications = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit,' \
        ' sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'

    p1.description = 'Est ante in nibh mauris cursus mattis molestie a. Dui nunc mattis' \
        'enim ut tellus. Facilisis volutpat est velit egestas dui. Nec feugiat nisl pretium' \
        ' fusce id velit ut tortor pretium. Donec et odio pellentesque diam volutpat commodo sed.' \
        ' Commodo elit at imperdiet dui accumsan sit amet. Id donec ultrices tincidunt arcu' \
        ' non sodales neque sodales. Vitae congue mauris rhoncus aenean vel elit. ' \
        'Ultricies tristique nulla aliquet enim tortor. Lectus proin nibh nisl condimentum.'
    p1.time_commitment = 20
    p1.research_fields = fields[-4:-1]
    p1.title = 'Nunc faucibus'

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

    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with correct credentials
    THEN check that the response is valid and login is succesfull 
    """
    response = test_client.post('/login', 
                          data=dict(username='Student123', password='123',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == STATUS_CODE_SUCCESS
    assert b"Welcome to the Cougar Research Application Portal!" in response.data

    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data
    assert b"Please log in to access this page." in response.data 
    
def test_login_logout(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with correct credentials
    THEN check that the response is valid and login is succesfull 
    """
    response = test_client.post('/login', 
                          data=dict(username='Student123', password='123',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Cougar Research Application Portal" in response.data

    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data
    
def test_create_position(request,test_client,init_database):
    #first login
    response = test_client.post('/login', 
                          data=dict(username='Faculty123', password='123',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Cougar Research Application Portal" in response.data
    
    #test the create_position form 
    response = test_client.get('/create_position')
    assert response.status_code == 200
    assert b"Cougar Research Application Portal" in response.data
    #test creating a position
    f1 = db.session.query(user_models.Faculty).filter(user_models.Faculty.username=='Faculty123')
    fields = db.session.query(position_models.ResearchField).all()
    p1 = create_position(fields)
    response = test_client.post('/create_position', 
                    data=p1,
                    follow_redirects = True)
    assert response.status_code == 200
    p = db.session.query(position_models.Position).filter(position_models.Position.title =='Nunc faucibus')
    assert p.first().title == 'Nunc faucibus'
    assert p.first().time_commitment == 20
    assert p.first().start_date == datetime.utcnow()
    assert p.count() == 1
    assert b"Position successfully created." in response.data
    assert b"Cougar Research Application Portal" in response.data
    
def test_index(test_client):
    response = test_client.get('/index', 
                    follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data
    assert b"Cougar Research Application Portal" in response.data
    
def test_view_applied_positions(test_client):
    fields = db.session.query(position_models.ResearchField).all()
    student = create_student()
    position = create_position(fields)
    app = create_application(student, position)
    response = test_client.get('/view_applied_positions', 
                data=[position, student],
                follow_redirects = True)
    assert response.status_code == 200
    assert b"Your Applied Positions" in response.data
    
def test_position(test_client):
    p1 = create_position()
    response = test_client.get('/position<pos_id>', 
                data=p1,
                follow_redirects = True)
    assert response.status_code == 200
    assert b"Return to main page" in response.data

def test_view_applicamts(test_client):
    position = create_position()
    response = test_client.get('/view_applicants', 
            data=position,
            follow_redirects = True)
    assert response.status_code == 200
    assert b"Your Active Research Positions" in response.data
    
def test_apply(test_client):
    #first login
    response = test_client.post('/login', 
                          data=dict(username='Student123', password='123',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Cougar Research Application Portal" in response.data
    
    position = create_position()
    faculty = user_models.User.query.filter_by(id=position.faculty_id).first()
    
    #test the application form 
    response = test_client.get('/apply<pos_id>')
    assert response.status_code == 200
    
    response = test_client.post('apply/<pos_id>',
                                data=[position, faculty, position.id],
                                follow_redirects = True)
    
    assert response.status_code == 200
    assert b"Submit" in response.data
    assert b"Cougar Research Application Portal" in response.data

def test_edit_student(test_client):
   #first login
    response = test_client.post('/login', 
                          data=dict(username='Student123', password='123',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Cougar Research Application Portal" in response.data
    
    student = create_student()
    
    student.first_name = "New First Name"
    
    response = test_client.get('/edit',
                            data=student,
                            follow_redirects = True)
    assert response.status_code == 200
    assert b"Edit Prior Experience" in response.data
    assert b"Edit Technical Electives" in response.data
    assert b"Cougar Research Application Portal" in response.data
    assert student.first_name == "New First Name"
    
def test_edit_faculty(test_client):
    #first login
    response = test_client.post('/login', 
                          data=dict(username='Faculty123', password='123',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Cougar Research Application Portal" in response.data
    
    faculty = create_faculty()
    
    faculty.first_name = "New First Name"
    
    response = test_client.get('/edit',
                            data=faculty,
                            follow_redirects = True)
    assert response.status_code == 200
    assert b"Edit Prior Experience" in response.data
    assert b"Edit Technical Electives" in response.data
    assert b"Cougar Research Application Portal" in response.data
    assert faculty.first_name == "New First Name"
    
    
    
    


    
    


