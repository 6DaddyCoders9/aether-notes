from datetime import datetime, timezone
from core.redis_client import redis_client

BLACKLIST_PREFIX = "bl:"

def blacklist_token(jti: str, expires_at: datetime):
    now = datetime.now(timezone.utc)
    ttl = int((expires_at - now).total_seconds())
    if ttl > 0:
        redis_client.set(f"{BLACKLIST_PREFIX}{jti}", "true", ex=ttl)

def is_token_blacklisted(jti: str) -> bool:
    return redis_client.exists(f"{BLACKLIST_PREFIX}{jti}") == 1
