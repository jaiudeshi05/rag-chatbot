from redis import Redis

from app.core.config import settings


class RedisService:
    def __init__(self) -> None:
        self.client = Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )

    def ping(self) -> bool:
        return self.client.ping()


redis = RedisService()