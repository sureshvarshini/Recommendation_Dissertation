from decouple import config
import os

BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIRECTORY, 'profile.db')
    SQLALCHEMY_BINDS = {
        'food': "sqlite:///" + os.path.join(BASE_DIRECTORY, 'food.db'),
        'rating': "sqlite:///" + os.path.join(BASE_DIRECTORY, 'rating.db'),
        'water': "sqlite:///" + os.path.join(BASE_DIRECTORY, 'water.db'),
        'activity': "sqlite:///" + os.path.join(BASE_DIRECTORY, 'activity.db'),
        'adl': "sqlite:///" + os.path.join(BASE_DIRECTORY, 'adl.db')
    }
    SQLALCHEMY_ECHO = False
    DEBUG = True
    PROPAGATE_EXCEPTIONS = config('PROPAGATE_EXCEPTIONS', cast=bool) 
    CACHE_TYPE = config('CACHE_TYPE')
    CACHE_DEFAULT_TIMEOUT = config('CACHE_DEFAULT_TIMEOUT')
