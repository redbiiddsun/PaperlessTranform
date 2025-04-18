import uuid

from datetime import datetime, timezone
from sqlmodel import JSON, Column, Field, SQLModel

from app.common.time import utc_now

class Forms(SQLModel, table=True):
    __tablename__ = "form"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    name: str

    schemas: dict = Field(sa_column=Column(JSON), default={})

    userId: uuid.UUID = Field(default=None, foreign_key="user.id")

    requiredLogin: bool = Field(default=False)
    
    createdAt: datetime = Field(default_factory=utc_now)

    updatedAt: datetime = Field(default_factory=utc_now)
    