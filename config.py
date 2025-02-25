import os
from dotenv import load_dotenv


load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    if os.getenv('FLASK_ENV') == 'development':
        load_dotenv()

    SECRET_KEY = os.getenv('SECRET_KEY')
    if SECRET_KEY is None:
        raise ValueError('Please set a secret key')

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    if SQLALCHEMY_DATABASE_URI is None:
        raise ValueError('Please set a database connection string')

    SQLALCHEMY_TRACK_MODIFICATIONS = False