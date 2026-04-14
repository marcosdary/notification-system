from redis.asyncio import Redis
from app.config.settings import settings

redis_client = Redis.from_url(
    url=settings.REDIS_URL, 
    decode_responses=True
)

