from datetime import datetime, time, timedelta
import redis.asyncio as redis

from config import REDIS_HOST, REDIS_PORT, REDIS_DB


redis_client = redis.from_url(
    f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
    encoding="utf-8",
    decode_responses=True,
)

def seconds_until_reset() -> int:
    """
    Считаем, сколько секунд до ближайшего ежедневного сброса в 14:11.
    Если сейчас после 14:11, то до завтрашнего 14:11.
    """
    now = datetime.now()
    reset = datetime.combine(now.date(), time(14, 11))
    if now >= reset:
        reset += timedelta(days=1)
    return int((reset - now).total_seconds())