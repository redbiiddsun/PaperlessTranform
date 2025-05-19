from typing import Optional
from fastapi import Cookie
import jwt
import time

from pydantic import BaseModel

from app.common.errors.user_error import Unauthorized
from app.common.time import utc_now
from app.config import settings

if(settings.SECRET_KEY is None):
    raise Exception("SECRET_KEY is not set")

class TokenPayload(BaseModel):
    user_id: str | None
    expired: int | None

def signJwt(sub: str):

    payload = {
    'iss': 'paperlesstranfrom',
    'sub': str(sub),
    'iat': int(time.time()),
    'exp': int(time.time()) + 3600 * 24,
    }

    if(settings.SECRET_KEY is None):
        raise Exception("SECRET_KEY is not set")

    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return encoded_jwt

def decodeJwt(token: str) -> Optional[TokenPayload]:

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        return TokenPayload(
            user_id=payload.get("sub"),
            expired=payload.get("exp")
        )

    except jwt.InvalidTokenError:
        return None