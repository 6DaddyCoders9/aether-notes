import os
import secrets
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from jose import JWTError, jwt
from core.auth_utils import is_token_blacklisted

# Use env var for SECRET_KEY in production
SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    jti = str(uuid4())
    # exp must be an int (epoch seconds), not datetime
    to_encode.update({"exp": int(expire.timestamp()), "jti": jti})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    """
    Verifies JWT signature, expiry, and blacklist.
    Returns payload dict if valid, else None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        jti = payload.get("jti")
        if not email or not jti:
            return None
        if is_token_blacklisted(jti):
            return None
        return payload
    except JWTError:
        return None
