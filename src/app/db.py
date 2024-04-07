import os

from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


PRIMARY_DATABASE_URL = os.environ["PRIMARY_DATABASE_URL"]
primary_engine = create_async_engine(PRIMARY_DATABASE_URL, echo=False, future=True)
primary_async_session = async_sessionmaker(primary_engine, class_=AsyncSession, expire_on_commit=False)


async def get_primary_session() -> AsyncSession:
    async with primary_async_session() as session:
        yield session


REPLICA_DATABASE_URL = os.environ["REPLICA_DATABASE_URL"]
replica_engine = create_async_engine(REPLICA_DATABASE_URL, echo=False, future=True)
replica_async_session = async_sessionmaker(replica_engine, class_=AsyncSession, expire_on_commit=False)


async def get_replica_session() -> AsyncSession:
    async with replica_async_session() as session:
        yield session


async def init_db():
    async with primary_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
