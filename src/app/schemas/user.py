from enum import Enum

from sqlmodel import SQLModel, Field


class ColorThemeMode(str, Enum):
    light = 'light'
    dark = 'dark'


class UserNames(SQLModel):
    first_name: str = Field(index=True, nullable=False)
    last_name: str = Field(index=True, nullable=False)


class UserBase(UserNames):
    color_theme: ColorThemeMode = Field(default=ColorThemeMode.light)
