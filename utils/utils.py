from redis import Redis
from core.project_settings import settings


def get_redis_client():
    s = settings()
    return Redis(host=s.REDIS_HOST_URL, port=s.REDIS_HOST_PORT, db=0, decode_responses=True,
                 password=s.REDIS_HOST_PASSWORD)
