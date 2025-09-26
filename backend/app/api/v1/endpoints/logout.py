# backend/app/api/v1/endpoints/logout.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timezone
from app.core.security import SECRET_KEY, ALGORITHM, verify_token
from app.core.auth_utils import blacklist_token
from jose import jwt

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

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")
        exp = payload.get("exp")
        if not jti or not exp:
            raise HTTPException(status_code=400, detail="Invalid token payload")

        expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)
        blacklist_token(jti, expires_at) 

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to blacklist token: {e}")

    return {"message": "Successfully logged out"}
