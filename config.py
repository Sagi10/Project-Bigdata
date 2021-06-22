import os


# Database connection setup
class Config(object):
    SERVER = ''
    DATABASE = ''
    DRIVER = ''
    USERNAME = ''
    PASSWORD = ''

    SQLALCHEMY_DATABASE_URI = f'mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or ''  # Set the Secret_key Config
