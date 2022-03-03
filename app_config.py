from flask_redis import Redis
from flask import Flask
from environs import Env

app = Flask(__name__, template_folder='templates')

env = Env()
env.read_env()
redis_host = env.str('REDIS_HOST')
redis_port = env.str('REDIS_PORT')
redis_password = env.str('REDIS_PASSWORD')
app.config['REDIS_HOST'] = redis_host
app.config['REDIS_PORT'] = redis_port
app.config['REDIS_PASSWORD'] = redis_password

redis = Redis(app)