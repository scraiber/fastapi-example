from fastapi import HTTPException
from fastapi import status as http_status
from fastapi import APIRouter

from app.s3 import upload_to_s3, get_from_s3, delete_from_bucket

router = APIRouter()


@router.post("/", status_code=201)
async def create_s3_item(key: str, value: str):
    await upload_to_s3(file=value.encode('utf-8'), key=key)


@router.get("/", status_code=200, response_model=bytes)
async def get_s3_item(key: str) -> bytes:
    out = await get_from_s3(key=key)
    if out == b'':
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Could not retrieve item!")
    return out


@router.put("/", status_code=200)
async def update_s3_item(key: str, value: str):
    await upload_to_s3(file=value.encode('utf-8'), key=key)


@router.delete("/", status_code=200)
async def delete_s3_item(key: str):
    await delete_from_bucket(key=key)
