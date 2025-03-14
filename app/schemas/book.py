from pydantic import BaseModel, constr, conint, field_validator
from typing import Optional
from datetime import datetime

ALLOWED_GENRES = {"Fiction", "Non-Fiction", "Science", "History"}


class AuthorBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)


class AuthorCreate(AuthorBase):
    pass


class AuthorOut(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: constr(strip_whitespace=True, min_length=1)
    published_year: conint(ge=1800, le=datetime.now().year)
    genre: constr(strip_whitespace=True, min_length=1)
    author_name: constr(strip_whitespace=True, min_length=1)

    @field_validator("genre")
    def validate_genre(cls, v):
        if v not in ALLOWED_GENRES:
            raise ValueError(f"Genre must be one of: {ALLOWED_GENRES}")
        return v


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[constr(strip_whitespace=True, min_length=1)]
    published_year: Optional[conint(ge=1800, le=datetime.now().year)]
    genre: Optional[constr(strip_whitespace=True, min_length=1)]
    author_name: Optional[constr(strip_whitespace=True, min_length=1)]

    @field_validator("genre")
    def validate_genre(cls, v):
        if v and v not in ALLOWED_GENRES:
            raise ValueError(f"Genre must be one of: {ALLOWED_GENRES}")
        return v


class BookOut(BaseModel):
    id: int
    title: str
    published_year: int
    genre: str
    author: AuthorOut

    class Config:
        orm_mode = True
