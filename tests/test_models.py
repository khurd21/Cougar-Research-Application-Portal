

import warnings
warnings.filterwarnings('ignore')


from tests import TestConfig
from app import create_app, db
import unittest

import app.Model.user_models as user_models
import app.Model.experience_models as experience_models
import app.Model.position_models as position_models

VERBOSITY = 2

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

        s1 = user_models.Student(username='test_student', email='test_email@test.com',
                                    major='test_major', phone_number='1234567890',
                                    first_name='test', last_name='student',
                                    wsu_id=123456789, gpa=2.0)
        s1.set_password('123')
        s1.save_to_db()

        ## Both queries should return the same object
        s1_q = user_models.Student.query.filter_by(username='test_student').first()
        s2_q = user_models.User.query.filter_by(username='test_student').first()
        self.assertEqual(s1, s1_q)
        self.assertEqual(s1,s2_q)
        return


    def test_create_faculty_account(self):
        
        f1 = user_models.Faculty(username='test_faculty', email='test_faculty@test.com',
                                    phone_number='1234567890', wsu_id=123446789,
                                    first_name='test', last_name='faculty'
                                    )
        f1.set_password('123')
        f1.save_to_db()

        ## Both queries should return the same object
        f1_q = user_models.Faculty.query.filter_by(username='test_faculty').first()
        f2_q = user_models.User.query.filter_by(username='test_faculty').first()
        self.assertEqual(f1, f1_q)
        self.assertEqual(f1,f2_q)
        return

if __name__ == '__main__':
    unittest.main(verbosity=VERBOSITY)
