import string
import random

import redis.asyncio as redis

from app import redis_pool


async def generate_random_string(k: int = 10):
    return ''.join(random.choices(string.ascii_lowercase, k=k))


async def generate_random_bytes_string(k: int = 10):
    return (await generate_random_string(k)).encode('utf-8')


async def create_random_redis_record(key: str, value: str):
    client = redis.Redis.from_pool(redis_pool)
    await client.set(key, value)
    await client.aclose()


async def get_redis_record(key: str):
    client = redis.Redis.from_pool(redis_pool)
    value = await client.get(key)
    await client.aclose()
    return value
