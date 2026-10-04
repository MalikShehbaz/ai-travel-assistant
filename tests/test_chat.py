from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_chat_validation():
    response = client.post(
        "/api/v1/chat",
        json={},
    )

    assert response.status_code == 422