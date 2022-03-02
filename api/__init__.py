from flask_redis import Redis
from flask import Flask, url_for, current_app
from environs import Env

app = Flask(__name__)

env = Env()
env.read_env()
redis_host = env.str('REDIS_HOST')
redis_port = env.str('REDIS_PORT')
redis_password = env.str('REDIS_PASSWORD')
app.config['SERVER_NAME'] = '127.0.0.1:5000'
app.config['REDIS_HOST'] = redis_host
app.config['REDIS_PORT'] = redis_port
app.config['REDIS_PASSWORD'] = redis_password

redis = Redis(app)