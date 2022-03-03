import pytest
from flask_redis import Redis
from app_factory import create_app


@pytest.fixture()
def app():
    app = create_app()
    redis = Redis()
    app.config.from_object('config.DevConfig')
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_main_page(client):
    response = client.get("/")
    assert b"Я сейчас буду сокращать все ссылки!" in response.data
