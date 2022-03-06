from os import path
from environs import Env


env = Env()
env.read_env()
basedir = path.abspath(path.dirname(__file__))


class Config:
    SECRET_KEY = env.str('SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    REDIS_HOST = env.str('REDIS_HOST')
    REDIS_PORT = env.str('REDIS_PORT')
    REDIS_PASSWORD = env.str('REDIS_PASSWORD')


class ProdConfig(Config):
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True
    TESTING = True
