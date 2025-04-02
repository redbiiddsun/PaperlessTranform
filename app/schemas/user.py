import uuid

from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    __tablename__ = "user"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    email: str = Field(unique=True)

    password: str

    firstname: str

    lastname: str

    isActive: bool = Field(default=True)

    createdAt: datetime = Field(default_factory=datetime.now)

    updatedAt: datetime = Field(default_factory=datetime.now)
    