from pydantic import BaseModel, Field


class SettingsSchema(BaseModel):
    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_PORT: int
    PG_DB: str

    SECRET_KEY: str
    ALGORITHM: str
