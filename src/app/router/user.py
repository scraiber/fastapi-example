import uuid
from typing import List

from fastapi import APIRouter, Depends

from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.user import UserCRUD
from app.db import get_primary_session, get_replica_session
from app.models.user import User
from app.schemas.user import UserBase, UserNames

router = APIRouter()


@router.post("/", status_code=201, response_model=User)
async def create_user(user_names: UserNames, session: AsyncSession = Depends(get_primary_session)) -> User:
    return await UserCRUD(session=session).create(user_names=user_names)


@router.get("/", status_code=200, response_model=User)
async def get_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_replica_session)) -> User:
    return await UserCRUD(session=session).get(user_id=user_id)


@router.get("/all", status_code=200, response_model=List[User])
async def get_all_users(session: AsyncSession = Depends(get_replica_session)) -> List[User]:
    return await UserCRUD(session=session).get_all()


@router.put("/", status_code=200, response_model=User)
async def update_user(user_id: uuid.UUID, user_base: UserBase, session: AsyncSession = Depends(get_primary_session)) -> User:
    return await UserCRUD(session=session).update_user(user_id=user_id, user_base=user_base)


@router.delete("/", status_code=200, response_model=User)
async def delete_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_primary_session)) -> User:
    return await UserCRUD(session=session).delete_user(user_id=user_id)
