import uuid

from typing import Optional
from datetime import datetime, timedelta
from sqlmodel import Field, SQLModel

class Otp(SQLModel, table=True):
    __tablename__ = "otp"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    otp: str

    referenceCode: str

    attempted: int = Field(default=0)

    userId: uuid.UUID = Field(foreign_key="user.id")

    isVerified: bool = Field(default=False)

    expireAt: datetime = Field(default_factory=lambda: datetime.now() + timedelta(minutes=5))

    createdAt: datetime = Field(default_factory=datetime.now)