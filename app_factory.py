from flask import Flask
from flask_redis import Redis


def create_app():

    app = Flask(__name__)
    redis = Redis()
    app.config.from_object('config.DevConfig')
    redis.init_app(app)

    return app
