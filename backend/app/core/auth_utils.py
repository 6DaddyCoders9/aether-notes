# backend/core/auth_utils.py
from datetime import datetime, timezone
from core.redis_client import redis_client

BLACKLIST_PREFIX = "bl:"  # Prefix for blacklisted tokens

def blacklist_token(jti: str, expires_at: datetime):
    """
    Add token jti to the blacklist until it expires.
    """
    # Store in Redis with TTL = seconds until expiry
    now = datetime.now(timezone.utc)
    ttl = int((expires_at - now).total_seconds())
    if ttl > 0:
        redis_client.set(f"{BLACKLIST_PREFIX}{jti}", "true", ex=ttl)

def is_token_blacklisted(jti: str) -> bool:
    """
    Check if a token jti is in the blacklist.
    """
    return redis_client.exists(f"{BLACKLIST_PREFIX}{jti}") == 1
