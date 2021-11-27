# __init__.py
# Initializer for the tests to use


from config import Config
import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ROOT_PATH = f'../{base_dir}'
