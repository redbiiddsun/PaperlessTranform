import uuid

from datetime import datetime
from sqlmodel import JSON, Column, Field, SQLModel

class Form(SQLModel, table=True):
    __tablename__ = "form"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    name: str

    schema: dict = Field(sa_column=Column(JSON), default={})

    user_id: uuid.UUID = Field(default=None, foreign_key="user.id")

    requiedLogin: bool = Field(default=False)

    created_at: datetime = Field(default_factory=datetime.now())

    updated_at: datetime = Field(default_factory=datetime.now())
    