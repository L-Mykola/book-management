from pydantic import BaseModel, constr


class UserCreate(BaseModel):
    username: constr(strip_whitespace=True, min_length=3)
    password: constr(min_length=6)


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
