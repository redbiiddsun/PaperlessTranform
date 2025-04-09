import uuid

from typing import Optional
from datetime import datetime, timedelta, timezone
from sqlmodel import Field, SQLModel

from app.common.time import utc_now

class ResetPasswordSession(SQLModel, table=True):
    __tablename__ = "reset_password_session"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    token: str

    userId: uuid.UUID = Field(foreign_key="user.id")

    isReset: bool = Field(default=False)

    expireAt: datetime = Field(default_factory=lambda: utc_now() + timedelta(minutes=5))

    createdAt: datetime = Field(default_factory=utc_now)