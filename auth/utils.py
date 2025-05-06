from datetime import timedelta
import datetime
import uuid
import jwt
from core.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_timedelta: timedelta | None = None,
    expire_minutes: int = settings.auth_jwt.access_token_expires_minutes,
):
    """
    Encode a JWT token.
    """
    to_encode = payload.copy()
    now = datetime.datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + datetime.timedelta(minutes=expire_minutes)

    to_encode.update(
        exp=expire,
        iat=now,
    )

    encoded = jwt.encode(to_encode, private_key, algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded
