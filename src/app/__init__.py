import os
from datetime import datetime, timezone

from dotenv import load_dotenv
import redis.asyncio as redis


if os.getenv('VAULT_PATH'):
    load_dotenv(dotenv_path=os.environ['VAULT_PATH'])


REDIS_MAX_CONNECTIONS = int(os.environ.get('REDIS_MAX_CONNECTIONS', 100))
REDIS_URL = os.environ['REDIS_URL']
redis_pool = redis.ConnectionPool.from_url(REDIS_URL, max_connections=REDIS_MAX_CONNECTIONS)

S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']


def generate_utc_time() -> datetime:
    return datetime.now(tz=timezone.utc).replace(tzinfo=None)
