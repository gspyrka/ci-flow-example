from fastapi.testclient import TestClient

from src.sample_api.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_user():
    response = client.get("/users/123")

    assert response.status_code == 200
    assert response.json() == {"user_id": 123}


def test_get_user_invalid_id():
    response = client.get("/users/abc")

    assert response.status_code == 422