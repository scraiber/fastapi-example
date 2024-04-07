import redis.asyncio as redis

from fastapi import HTTPException
from fastapi import status as http_status
from fastapi import APIRouter

from app import redis_pool

router = APIRouter()


@router.post("/", status_code=201)
async def create_redis_item(key: str, value: str):
    client = redis.Redis.from_pool(redis_pool)
    await client.set(key, value)
    await client.aclose()


@router.get("/", status_code=200, response_model=str)
async def get_redis_item(key: str) -> str:
    client = redis.Redis.from_pool(redis_pool)
    value = await client.get(key)
    await client.aclose()

    if not value:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Could not retrieve item!")

    return value


@router.put("/", status_code=200)
async def update_redis_item(key: str, value: str):
    client = redis.Redis.from_pool(redis_pool)
    await client.set(key, value)
    await client.aclose()


@router.delete("/", status_code=200)
async def delete_redis_item(key: str):
    client = redis.Redis.from_pool(redis_pool)
    await client.delete(key)
    await client.aclose()
