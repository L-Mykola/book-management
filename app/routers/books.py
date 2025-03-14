import csv
import io
import json

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional, List

from app.crud import books as CRUD
from app.schemas.book import BookOut, BookUpdate, BookCreate
from app.models import User
from app.utils.auth import decode_access_token
from app.database import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.post("/", response_model=BookOut)
def create_book(book: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = CRUD.create_book(db, book)
    return result


@router.get("/", response_model=List[BookOut])
def get_books(
    title: Optional[str] = Query(None),
    genre: Optional[str] = Query(None),
    published_year_from: Optional[int] = Query(None),
    published_year_to: Optional[int] = Query(None),
    sort_by: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    filters = {}
    if title:
        filters["title"] = title
    if genre:
        filters["genre"] = genre
    if published_year_from:
        filters["published_year_from"] = published_year_from
    if published_year_to:
        filters["published_year_to"] = published_year_to

    skip = (page - 1) * page_size
    books = CRUD.get_books(db, skip=skip, limit=page_size, filters=filters, sort_by=sort_by)
    return books


@router.get("/{book_id}", response_model=BookOut)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book = CRUD.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_book = CRUD.update_book(db, book_id, book_update)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success = CRUD.delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book deleted successfully"}


@router.post("/bulk-import")
async def bulk_import(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contents = await file.read()
    books_created = []
    if file.filename.endswith(".json"):
        try:
            data = json.loads(contents)
            if not isinstance(data, list):
                raise HTTPException(status_code=400, detail="JSON має містити список записів")
            for record in data:
                book_data = BookCreate(**record)
                book = CRUD.create_book(db, book_data)
                books_created.append(book)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif file.filename.endswith(".csv"):
        try:
            decoded = contents.decode("utf-8")
            reader = csv.DictReader(io.StringIO(decoded))
            for row in reader:
                book_data = BookCreate(
                    title=row.get("title"),
                    published_year=int(row.get("published_year")),
                    genre=row.get("genre"),
                    author_name=row.get("author_name")
                )
                book = CRUD.create_book(db, book_data)
                books_created.append(book)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Непідтримуваний тип файлу. Завантажте JSON або CSV файл.")
    return {"imported": len(books_created), "books": books_created}
