

import warnings
warnings.filterwarnings('ignore')


from tests import TestConfig
from app import create_app, db

from datetime import datetime, timedelta
import unittest

import app.Model.user_models as user_models
import app.Model.experience_models as experience_models
import app.Model.position_models as position_models
import app.Controller.routes as routes

VERBOSITY = 2


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
                                    faculty_id=faculty.id,
                                    required_qualifications='test_qualifications', start_date=datetime.utcnow(),
                                    end_date=datetime.utcnow() + timedelta(days=1)
                                    )

def create_application(student, position):
    return position_models.Application(student_id=student.id, position_id=position.id,
                                        description='test_description',
                                        ref_name='test_ref_name', ref_email='test_ref_email'
                                        )


def create_status():
    return position_models.Status(status='Pending')


class TestModels(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        return 

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        return 


    def test_password_hashing(self):
        user = user_models.User()
        user.set_password('123')
        self.assertTrue(user.check_password('123'))
        self.assertFalse(user.check_password('1234'))
        return
        

    def test_create_student_account(self):

        s1 = create_student()
        s1.set_password('123')
        s1.save_to_db()

        ## Both queries should return the same object
        s1_q = user_models.Student.query.filter_by(username='test_student').first()
        s2_q = user_models.User.query.filter_by(username='test_student').first()
        self.assertEqual(s1, s1_q)
        self.assertEqual(s1,s2_q)
        return


    def test_create_faculty_account(self):
        
        f1 = create_faculty() 
        f1.set_password('123')
        f1.save_to_db()

        ## Both queries should return the same object
        f1_q = user_models.Faculty.query.filter_by(username='test_faculty').first()
        f2_q = user_models.User.query.filter_by(username='test_faculty').first()
        self.assertEqual(f1, f1_q)
        self.assertEqual(f1,f2_q)
        return

    
    def test_create_position(self):

        f1 = create_faculty()
        f1.save_to_db()
        p1 = create_position(f1)
        p1.save_to_db()

        p1_q = position_models.Position.query.filter_by(title='test_position').first()
        self.assertEqual(p1, p1_q)
        self.assertIn(p1, f1.posted_positions)
        return

    
    def test_create_application(self):
    
        f1 = create_faculty()
        f1.save_to_db()
        s1 = create_student()
        s1.save_to_db()

        p1 = create_position(f1)
        p1.save_to_db()
        a1 = create_application(s1, p1)
        status1 = create_status()
        status1.save_to_db()
        a1.status_id = status1.id
        a1.save_to_db()

        s1.applied_positions.append(p1)
        p1.application_forms.append(a1)
        db.session.commit()

        a1_q = position_models.Application.query.filter_by(student_id=s1.id, position_id=p1.id).first()
        self.assertEqual(a1, a1_q)
        self.assertEqual(a1.status_id, status1.id)
        self.assertIn(p1, s1.applied_positions)
        self.assertIn(a1, p1.application_forms)
        return


if __name__ == '__main__':
    unittest.main(verbosity=VERBOSITY)
