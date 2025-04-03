from pydantic import root_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DATABASE_USER: str

    DATABASE_PASSWORD: str

    DATABASE_HOST: str

    DATABASE_PORT: int

    DATABASE_NAME: str

    DATABASE_URL: str

    SECRET_KEY: str

    SMTP_HOST: str

    SMTP_PORT: int

    SMTP_USER: str

    SMTP_PASSWORD: str

    DEBUG: bool = False  

    class Config:
        env_file = ".env"  
        env_file_encoding = "utf-8"

settings = Settings()
