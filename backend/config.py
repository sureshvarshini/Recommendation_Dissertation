from decouple import config
import os

BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIRECTORY, 'profile.db')
    SQLALCHEMY_BINDS = {
        'food': "sqlite:///" + os.path.join(BASE_DIRECTORY, 'food.db'),
        'rating': "sqlite:///" + os.path.join(BASE_DIRECTORY, 'rating.db')
    }
    SQLALCHEMY_ECHO = True
    DEBUG = True
    PROPAGATE_EXCEPTIONS= config('PROPAGATE_EXCEPTIONS', cast=bool) 
