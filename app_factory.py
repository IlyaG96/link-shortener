from flask import Flask
from flask_redis import Redis
import link_shortener


def create_app():

    app = Flask(__name__)
    app.register_blueprint(link_shortener.bp)
    redis = Redis()
    app.config.from_object('config.DevConfig')
    redis.init_app(app)

    return app
