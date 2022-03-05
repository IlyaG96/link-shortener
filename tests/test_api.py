import random
from string import ascii_letters
import pytest
from app_factory import create_app
from link_shortener import Responses

TEST_LINK_NAME = ''.join(random.choice(ascii_letters) for letter in range(10))
TEST_URL = 'https://google.com'  # change this to any existing url


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


def test_status_200(client):
    response = client.get('/')
    assert '200 OK' == response.status


def test_no_query_params_custom(client):
    response = client.get('/api/custom')
    assert Responses.NO_QUERY_PARAMS == response.json


def test_no_link_in_query_params_custom(client):
    response = client.get('/api/custom?name=ivan&')
    assert Responses.WRONG_QUERY_PARAMS == response.json


def test_no_name_in_query_params_custom(client):
    response = client.get('/api/custom?link=https://google.com')
    assert Responses.WRONG_QUERY_PARAMS == response.json


def wrong_name_in_query_params_custom(client):
    response = client.get('/api/custom?link=https://google.com&name=!!22й')
    assert Responses.NAME_ERROR == response.json


def test_1_incorrect_link_in_query_params_custom(client):
    response = client.get(f'/api/custom?link=https://googsssale.com&name={TEST_LINK_NAME}')
    assert Responses.INCORRECT_LINK == response.json


def test_2_incorrect_link_in_query_params_custom(client):
    response = client.get(f'/api/custom?link=htt://google.com&name={TEST_LINK_NAME}')
    assert Responses.INCORRECT_LINK == response.json


def test_add_new_link_to_db_custom(client):
    response = client.get(f'/api/custom?link={TEST_URL}&name={TEST_LINK_NAME}')
    assert TEST_LINK_NAME in response.json['message']


def test_get_new_link_from_db_custom(client):
    response = client.get(TEST_LINK_NAME)
    assert '302 FOUND' == response.status


def test_existed_link_in_query_params(client):
    response = client.get('/api/custom?link=https://google.com')
    assert Responses.WRONG_QUERY_PARAMS == response.json


def test_no_query_params_auto(client):
    response = client.get('/api/make-short')
    assert Responses.NO_QUERY_PARAMS == response.json


def test_wrong_query_params_auto(client):
    response = client.get('/api/make-short?name=ivan&')
    assert Responses.WRONG_QUERY_PARAMS == response.json


def test_no_link_in_query_params_auto(client):
    response = client.get('/api/make-short?link=')
    assert Responses.WRONG_QUERY_PARAMS == response.json


def test_1_incorrect_link_in_query_params_auto(client):
    response = client.get(f'/api/make-short?link=https://')
    assert Responses.INCORRECT_LINK == response.json


def test_2_incorrect_link_in_query_params_auto(client):
    response = client.get(f'/api/make-short?link=https://gmoglemooglr.com')
    assert Responses.INCORRECT_LINK == response.json


def test_existed_link_in_query_params_auto(client):
    response = client.get('/api/custom?link=https://google.com')
    assert Responses.WRONG_QUERY_PARAMS == response.json
