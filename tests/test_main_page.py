import time

import pytest
from app_factory import create_app
from link_shortener import Responses


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


def test_status_200(client):
    response = client.get('/')
    assert '200 OK' == response.status


def test_no_query_params(client):
    response = client.get('/api/custom')

    assert Responses.NOT_QUERY_PARAMS == response.json


def test_no_name_in_query_params(client):
    response = client.get('/api/custom?name=ivan&')
    assert Responses.WRONG_QUERY_PARAMS == response.json


def test_no_link_in_query_params(client):
    response = client.get('/api/custom?link=https://google.com')
    assert Responses.WRONG_QUERY_PARAMS == response.json


def test_1incorrect_link_in_query_params(client):
    response = client.get('/api/custom?link=https://googsssale.com&name=ivan')
    time.sleep(3)
    assert Responses.INCORRECT_LINK == response.json


def test_2incorrect_link_in_query_params(client):
    response = client.get('/api/custom?link=htt://google.com&name=ivan')
    assert Responses.INCORRECT_LINK == response.json


def test_existed_link_in_query_params(client):
    response = client.get('/api/custom?link=https://google.com')
    assert Responses.INCORRECT_LINK == response.json

