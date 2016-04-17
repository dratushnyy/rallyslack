from redis import Redis
from settings import REDIS_URL

redis_connection = Redis.from_url(REDIS_URL)
