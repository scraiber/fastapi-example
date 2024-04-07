import uuid
from typing import List

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserNames, UserBase


class UserCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_names: UserNames) -> User:
        user = User.model_validate(user_names)
        self.session.add(user)
        await self.session.commit()
        return user

    async def get(self, user_id: uuid.UUID, return_always: bool = False) -> User:
        res = await self.session.execute(select(User).where(User.user_id == user_id))
        user_return = res.one_or_none()

        if not return_always and not user_return:
            raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Could not retrieve user!")

        return user_return[0]

    async def get_all(self) -> List[User]:
        res = await self.session.execute(select(User))
        return [item[0] for item in res.all()]

    async def update_user(self, user_id: uuid.UUID, user_base: UserBase) -> User:
        user_return = await self.get(user_id=user_id)

        user_values = user_base.model_dump(exclude_unset=True)
        for k, v in user_values.items():
            setattr(user_return, k, v)

        self.session.add(user_return)
        await self.session.commit()
        return user_return

    async def delete_user(self, user_id: uuid.UUID) -> User:
        res = await self.session.execute(select(User).where(User.user_id == user_id))
        user_return = res.scalar_one_or_none()

        if not user_return:
            raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Could not retrieve user!")

        await self.session.delete(user_return)
        await self.session.commit()
        return user_return
