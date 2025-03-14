import pytest
import json
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


@pytest.fixture(scope="module")
def auth_token():
    username = "bookuser"
    password = "bookpass"
    client.post("/auth/signup", json={"username": username, "password": password})
    response = client.post(
        "/auth/login",
        data={"username": username, "password": password}
    )
    token = response.json()["access_token"]
    return token


def test_create_book(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post(
        "/books/",
        json={
            "title": "Test Book",
            "published_year": 2020,
            "genre": "Fiction",
            "author_name": "John Doe"
        },
        headers=headers
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author"]["name"] == "John Doe"
    global created_book_id
    created_book_id = data["id"]


def test_get_books(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/books/", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "title" in data[0]


def test_get_book_by_id(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response_create = client.post(
        "/books/",
        json={
            "title": "Another Book",
            "published_year": 2021,
            "genre": "Non-Fiction",
            "author_name": "Jane Smith"
        },
        headers=headers
    )
    book_id = response_create.json()["id"]
    response = client.get(f"/books/{book_id}", headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == book_id
    assert data["title"] == "Another Book"


def test_update_book(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response_create = client.post(
        "/books/",
        json={
            "title": "Book to Update",
            "published_year": 2019,
            "genre": "Science",
            "author_name": "Alice"
        },
        headers=headers
    )
    book_id = response_create.json()["id"]

    response_update = client.put(
        f"/books/{book_id}",
        json={
            "title": "Updated Book Title",
            "published_year": 2022,
            "genre": "History",
            "author_name": "Bob"
        },
        headers=headers
    )
    assert response_update.status_code == 200, response_update.text
    data = response_update.json()
    assert data["title"] == "Updated Book Title"
    assert data["genre"] == "History"
    assert data["author"]["name"] == "Bob"


def test_delete_book(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response_create = client.post(
        "/books/",
        json={
            "title": "Book to Delete",
            "published_year": 2018,
            "genre": "Fiction",
            "author_name": "Charlie"
        },
        headers=headers
    )
    book_id = response_create.json()["id"]

    response_delete = client.delete(f"/books/{book_id}", headers=headers)
    assert response_delete.status_code == 200, response_delete.text

    response_get = client.get(f"/books/{book_id}", headers=headers)
    assert response_get.status_code == 404


def test_bulk_import_json(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    books_data = [
        {
            "title": "Bulk Book 1",
            "published_year": 2020,
            "genre": "Fiction",
            "author_name": "Bulk Author 1"
        },
        {
            "title": "Bulk Book 2",
            "published_year": 2021,
            "genre": "Non-Fiction",
            "author_name": "Bulk Author 2"
        }
    ]
    json_data = json.dumps(books_data)
    files = {
        "file": ("books.json", json_data, "application/json")
    }
    response = client.post("/books/bulk-import", files=files, headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "imported" in data
    assert data["imported"] == 2


def test_bulk_import_csv(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    csv_content = "title,published_year,genre,author_name\n"
    csv_content += "CSV Book 1,2020,Fiction,CSV Author 1\n"
    csv_content += "CSV Book 2,2021,Non-Fiction,CSV Author 2\n"
    files = {
        "file": ("books.csv", csv_content, "text/csv")
    }
    response = client.post("/books/bulk-import", files=files, headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "imported" in data
    assert data["imported"] == 2
