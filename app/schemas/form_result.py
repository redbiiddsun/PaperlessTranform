import uuid

from typing import Optional
from datetime import datetime
from sqlmodel import JSON, Column, Field, SQLModel

class FormResult(SQLModel, table=True):

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    form_id: uuid.UUID = Field(default=None, foreign_key="form.id")

    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id", nullable=True)

    result: dict = Field(sa_column=Column(JSON), default={})

    created_at: datetime = Field(default_factory=datetime.now())
    