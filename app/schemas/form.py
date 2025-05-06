import uuid

from datetime import datetime
from sqlmodel import JSON, Column, Field, Relationship, SQLModel

from app.common.time import utc_now

class Forms(SQLModel, table=True):
    __tablename__ = "form"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    name: str

    schemas: list = Field(sa_column=Column(JSON), default={})

    width: str

    description: str | None = Field(default=None)
    
    userId: uuid.UUID = Field(foreign_key="user.id")

    requiredLogin: bool = Field(default=False)
    
    createdAt: datetime = Field(default_factory=utc_now)

    updatedAt: datetime = Field(default_factory=utc_now)

    # Relationships
    formResult: list["FormResult"] = Relationship(cascade_delete=True)
    