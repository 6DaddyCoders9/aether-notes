# backend/core/auth_utils.py
from datetime import datetime, timezone
from core.redis_client import redis_client

BLACKLIST_PREFIX = "bl:"  # Prefix for blacklisted tokens

def blacklist_token(token: str, expires_at: datetime):
    """
    Add a JWT to the blacklist until it expires.
    """
    # Store in Redis with TTL = seconds until expiry
    now = datetime.now(timezone.utc)
    ttl = int((expires_at - now).total_seconds())
    if ttl > 0:
        redis_client.set(f"{BLACKLIST_PREFIX}{token}", "true", ex=ttl)

def is_token_blacklisted(token: str) -> bool:
    """
    Check if a token is in the blacklist.
    """
    return redis_client.exists(f"{BLACKLIST_PREFIX}{token}") == 1
