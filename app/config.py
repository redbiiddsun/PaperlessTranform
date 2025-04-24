from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    ENV: str

    DOMAIN: str

    DATABASE_USER: str

    DATABASE_PASSWORD: str

    DATABASE_HOST: str

    DATABASE_PORT: int

    DATABASE_NAME: str

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
