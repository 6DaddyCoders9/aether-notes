import secrets
from core.auth_utils import is_token_blacklisted
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

# This should be a long, random, secret string.
# In production, set this via an environment variable.
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        exp: int = payload.get("exp")

        if email is None:
            return None
        
        # Check expiration manually just in case
        now_ts = int(datetime.now(timezone.utc).timestamp())
        if exp is not None and exp < now_ts:
            return None

        # Check if token is blacklisted
        if is_token_blacklisted(token):
            return None

        return email
    
    except JWTError:
        return None