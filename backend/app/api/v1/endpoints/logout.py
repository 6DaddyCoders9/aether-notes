# backend/app/api/v1/endpoints/logout.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timezone
from core.security import verify_token
from core.auth_utils import blacklist_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Can reuse your existing scheme

@router.post("/auth/logout", status_code=status.HTTP_200_OK)
def logout(token: str = Depends(oauth2_scheme)):
    """
    Logout the current user by blacklisting their JWT.
    """
    # Verify token and get user email
    email = verify_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # Decode token to get expiration
    from jose import jwt
    from core.security import SECRET_KEY, ALGORITHM

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp: int = payload.get("exp")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid token")

    if exp is None:
        raise HTTPException(status_code=400, detail="Token missing expiration")

    expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)

    # Blacklist the token
    blacklist_token(token, expires_at)

    return {"message": "Successfully logged out"}
