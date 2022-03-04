import pytest
from app_factory import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_status_200(client):
    response = client.get("/")
    assert '200 OK' == response.status