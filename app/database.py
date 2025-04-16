from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel
from app.config import settings

postgres_url = f"postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

## NOTED ####
# IF you need to debug the database connection, you can set the following environment variable:
# add a echo as true
# EX. engine = create_engine(postgres_url, echo=True)
##############
engine = create_engine(postgres_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

