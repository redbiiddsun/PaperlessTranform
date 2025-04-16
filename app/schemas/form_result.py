import uuid

from typing import Optional
from datetime import datetime, timezone
from sqlmodel import JSON, Column, Field, SQLModel

from app.common.time import utc_now

class FormResult(SQLModel, table=True):

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    formId: uuid.UUID = Field(default=None, foreign_key="form.id")

    userId: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id", nullable=True)

    result: dict = Field(sa_column=Column(JSON), default={})

    createdAt: datetime = Field(default_factory=utc_now)
    