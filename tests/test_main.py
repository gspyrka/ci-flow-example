from fastapi.testclient import TestClient

from sample_api.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "API działa"}


def test_health():
    response = client.get("/healtz")

    assert response.status_code == 200
    assert response.json() == {["ok"]}


def test_get_user():
    response = client.get("/items/123")

    assert response.status_code == 200
    assert response.json() == {"item_id": 123, "name": "Przykładowy przedmiot"}

