import uuid
from datetime import datetime

from sqlmodel import Field

from app import generate_utc_time
from app.schemas.user import UserBase


class User(UserBase, table=True):
    __tablename__ = "user"

    user_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False)
    created: datetime = Field(default_factory=generate_utc_time, nullable=False)
