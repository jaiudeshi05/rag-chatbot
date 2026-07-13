from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.project import Project


class User(BaseModel, table=True):
    __tablename__ = "users"

    google_sub: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    name: str
    profile_picture: str | None = None
    is_active: bool = Field(default=True)

    projects: list["Project"] = Relationship(back_populates="owner")