"""Flask configuration."""
from os import environ, path
from environs import Env
from flask_redis import Redis


env = Env()
env.read_env()
basedir = path.abspath(path.dirname(__file__))


class Config:
    """Base config."""
    SECRET_KEY = env.str('SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    REDIS_HOST = env.str('REDIS_HOST')
    REDIS_PORT = env.str('REDIS_PORT')
    REDIS_PASSWORD = env.str('REDIS_PASSWORD')


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    DATABASE_URI = environ.get('PROD_DATABASE_URI')


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    DATABASE_URI = environ.get('DEV_DATABASE_URI')