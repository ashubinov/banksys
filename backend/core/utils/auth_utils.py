from datetime import datetime, timedelta, timezone

import jwt

from backend.core.config import settings

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN = "access"
REFRESH_TOKEN = "refresh"


def encode_jwt(
    payload: dict,
    expire_timedelta: timedelta,
    key: str = settings.secret_key,
    algorithm: str = settings.algorithm,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    to_encode.update(exp=now + expire_timedelta, iat=now)
    return jwt.encode(to_encode, key, algorithm=algorithm)


def decode_jwt(
    token: str | bytes,
    key: str = settings.secret_key,
    algorithm: str = settings.algorithm,
) -> dict:
    """Бросает jwt.InvalidTokenError, если токен невалиден или истёк."""
    return jwt.decode(token, key, algorithms=[algorithm])


def create_jwt(token_type: str, token_data: dict, expire_timedelta: timedelta) -> str:
    payload = {TOKEN_TYPE_FIELD: token_type, **token_data}
    return encode_jwt(payload, expire_timedelta=expire_timedelta)


def create_access_token(username: str, expires_delta: timedelta | None = None) -> str:
    return create_jwt(
        token_type=ACCESS_TOKEN,
        token_data={"sub": username},
        expire_timedelta=expires_delta
        or timedelta(minutes=settings.access_token_expire_minutes),
    )


def create_refresh_token(username: str, expires_delta: timedelta | None = None) -> str:
    return create_jwt(
        token_type=REFRESH_TOKEN,
        token_data={"sub": username},
        expire_timedelta=expires_delta
        or timedelta(days=settings.refresh_token_expire_days),
    )
