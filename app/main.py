from fastapi import FastAPI
from app.routers import books, auth

app = FastAPI(
    title="Book Management System API",
    description="API для управління книгами з розширеними можливостями.",
    version="1.0.0"
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(books.router, prefix="/books", tags=["books"])

@app.get("/")
def read_root():
    return {"message": "Ласкаво просимо до Book Management System API"}