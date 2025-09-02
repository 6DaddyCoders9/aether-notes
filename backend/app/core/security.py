import secrets
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
        # Decode the token using your secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # The user's email is stored in the "sub" (subject) claim
        email: str = payload.get("sub")
        
        if email is None:
            # If the "sub" claim is missing, the token is invalid
            return None
            
        return email
    
    except JWTError:
        return None