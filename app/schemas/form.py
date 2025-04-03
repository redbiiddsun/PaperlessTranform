import uuid

from datetime import datetime
from sqlmodel import JSON, Column, Field, SQLModel

class Forms(SQLModel, table=True):
    __tablename__ = "form"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    name: str

    schema: dict = Field(sa_column=Column(JSON), default={})

    userId: uuid.UUID = Field(default=None, foreign_key="user.id")

    requiredLogin: bool = Field(default=False)
    
    createdAt: datetime = Field(default_factory=datetime.now())

    updatedAt: datetime = Field(default_factory=datetime.now())
    