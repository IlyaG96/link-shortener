from flask import Flask
from flask_redis import Redis
import server


def create_app():

    app = Flask(__name__)
    app.register_blueprint(server.bp)
    redis = Redis()
    app.config.from_object('config.DevConfig')
    redis.init_app(app)

    return app
