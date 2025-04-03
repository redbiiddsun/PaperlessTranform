import jwt
import datetime
import time

from app.config import settings

def signJwt(sub: str):

    payload = {
    'iss': 'paperlesstranfrom',
    'sub': str(sub),
    'iat': int(time.time()),
    'exp': int(time.time()) + 3600,
    }

    if(settings.SECRET_KEY is None):
        raise Exception("SECRET_KEY is not set")

    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return encoded_jwt

    
