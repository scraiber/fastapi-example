from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import init_db
from app.router import user, redis, s3


@asynccontextmanager
async def lifespan(app: FastAPI):
    # We create the tables in the database if they don't exist
    await init_db()
    yield


app = FastAPI(title="FastAPI example API for DB operations",
              description="This is the specification of the API for working with FastAPI and common databases",
              lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/user", tags=["user (postgresql_example)"])
app.include_router(redis.router, prefix="/redis", tags=["redis"])
app.include_router(s3.router, prefix="/s3", tags=["s3"])
