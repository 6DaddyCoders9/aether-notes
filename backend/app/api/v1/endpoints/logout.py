from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from datetime import datetime, timezone
from app.core.security import verify_token
from app.core.auth_utils import blacklist_token

router = APIRouter()
oauth2_scheme = HTTPBearer()

@router.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    jti = payload.get("jti")
    exp = payload.get("exp")
    if not jti or not exp:
        raise HTTPException(status_code=400, detail="Invalid token payload")

    expires_at = datetime.fromtimestamp(int(exp), tz=timezone.utc)
    blacklist_token(jti, expires_at)

    return None
