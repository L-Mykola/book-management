# Book Management System

A feature-rich book management system built with **FastAPI** for the backend and **PostgreSQL** for storage. This project demonstrates advanced CRUD operations, bulk data import, JWT-based authentication, and more.

## Features

- **CRUD Endpoints:** Create, retrieve, update, and delete books.
- **Bulk Import:** Import books from JSON or CSV files.
- **Filtering, Pagination & Sorting:** Easily query books based on different parameters.
- **JWT Authentication:** Secure endpoints for authenticated users.
- **Alembic Migrations:** Manage database schema changes with ease.
- **Testing:** Comprehensive tests for all endpoints using Pytest and FastAPI TestClient.


## Installation

1. **Clone the repository:**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

## Environment Variables
Create a .env file in the project root with the following example content
```bash
PG_USER=USER
PG_PASSWORD=PASSWORD
PG_HOST=HOST
PG_PORT=PORT
PG_DB=DB_NAME

SECRET_KEY = YOUR_SECRET_KEY
ALGORITHM = "HS256"
```
## Database Migrations with Alembic
This project uses Alembic to handle database schema migrations. Follow these steps to run migrations:
1. **Generate a new migration:**
After making changes to your models, run:
```bash
   alembic revision --autogenerate -m "Describe your changes here"
```
2. **Apply migrations to the database:**
```bash
   alembic upgrade head
```

## Running the Project
Start the FastAPI server using uvicorn:
```bash
   uvicorn app.main:app --reload
```
Access the API documentation at:

**Swagger UI: http://127.0.0.1:8000/docs** \
**ReDoc: http://127.0.0.1:8000/redoc**
