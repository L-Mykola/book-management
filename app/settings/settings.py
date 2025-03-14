import os
from dotenv import load_dotenv
from app.schemas.settings import SettingsSchema


class Settings:
    load_dotenv()

    PG_USER: SettingsSchema = os.getenv('PG_USER')
    PG_PASSWORD: SettingsSchema = os.getenv('PG_PASSWORD')
    PG_HOST: SettingsSchema = os.getenv('PG_HOST')
    PG_PORT: SettingsSchema = os.getenv('PG_PORT')
    PG_DB: SettingsSchema = os.getenv('PG_DB')

    SECRET_KEY: SettingsSchema = os.getenv('SECRET_KEY')
    ALGORITHM: SettingsSchema = os.getenv('ALGORITHM')


settings = Settings()
