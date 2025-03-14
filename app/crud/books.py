from sqlalchemy.orm import Session
from app import models
from app.schemas.book import BookCreate, BookUpdate


def get_author_by_name(db: Session, name: str):
    return db.query(models.Author).filter(models.Author.name == name).first()


def create_author(db: Session, name: str):
    author = models.Author(name=name)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def create_book(db: Session, book: BookCreate):
    author = get_author_by_name(db, book.author_name)
    if not author:
        author = create_author(db, book.author_name)
    new_book = models.Book(
        title=book.title,
        published_year=book.published_year,
        genre=book.genre,
        author_id=author.id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {
        "id": new_book.id,
        "title": new_book.title,
        "published_year": new_book.published_year,
        "genre": new_book.genre,
        "author": {"id": author.id, "name": author.name}
    }


def get_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book:
        return {
            "id": book.id,
            "title": book.title,
            "published_year": book.published_year,
            "genre": book.genre,
            "author": book.author  # Використовуємо визначене відношення
        }
    return None


def get_books(db: Session, skip: int = 0, limit: int = 10, filters: dict = None, sort_by: str = None):
    query = db.query(models.Book)
    filters = filters or {}
    if "title" in filters:
        query = query.filter(models.Book.title.ilike(f"%{filters['title']}%"))
    if "genre" in filters:
        query = query.filter(models.Book.genre == filters["genre"])
    if "published_year_from" in filters:
        query = query.filter(models.Book.published_year >= filters["published_year_from"])
    if "published_year_to" in filters:
        query = query.filter(models.Book.published_year <= filters["published_year_to"])
    if sort_by in {"title", "published_year", "genre"}:
        query = query.order_by(getattr(models.Book, sort_by))
    books = query.offset(skip).limit(limit).all()
    results = []
    for book in books:
        results.append({
            "id": book.id,
            "title": book.title,
            "published_year": book.published_year,
            "genre": book.genre,
            "author": book.author
        })
    return results


def update_book(db: Session, book_id: int, book_update: BookUpdate):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        return None

    if book_update.author_name:
        author = get_author_by_name(db, book_update.author_name)
        if not author:
            author = create_author(db, book_update.author_name)
        book.author_id = author.id

    if book_update.title:
        book.title = book_update.title
    if book_update.published_year:
        book.published_year = book_update.published_year
    if book_update.genre:
        book.genre = book_update.genre

    db.commit()
    db.refresh(book)
    return {
        "id": book.id,
        "title": book.title,
        "published_year": book.published_year,
        "genre": book.genre,
        "author": book.author
    }


def delete_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        return False
    db.delete(book)
    db.commit()
    return True
