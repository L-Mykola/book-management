import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine
from app.models import Base

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_signup():
    response = client.post(
        "/auth/signup",
        json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    assert data["username"] == "testuser"


def test_signup_duplicate():
    client.post("/auth/signup", json={"username": "duplicate", "password": "testpass"})
    response = client.post("/auth/signup", json={"username": "duplicate", "password": "testpass"})
    assert response.status_code == 400


def test_login():
    client.post("/auth/signup", json={"username": "loginuser", "password": "testpass"})
    response = client.post(
        "/auth/login",
        data={"username": "loginuser", "password": "testpass"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
