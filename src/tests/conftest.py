import asyncio

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import async_sessionmaker

import pytest_asyncio
from typing import Generator

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import primary_engine, replica_engine

from app.main import app


@pytest_asyncio.fixture
async def client() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def session() -> AsyncSession:
    async_session = async_sessionmaker(primary_engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as s:
        async with primary_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        yield s

    async with primary_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await primary_engine.dispose()
    await replica_engine.dispose()


pytestmark = pytest.mark.asyncio
