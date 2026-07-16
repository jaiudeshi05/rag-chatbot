from typing import TYPE_CHECKING
from uuid import UUID
from sqlmodel import Field, ForeignKey, Relationship
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.chat import Chat
    from app.models.document import Document
    from app.models.user import User


class Project(BaseModel, table=True):
    __tablename__ = "projects"
    user_id: UUID = Field(
    foreign_key="users.id",
    index=True,)
    name: str

    chunk_size: int = Field(default=500, ge=200, le=1000)
    chunk_overlap: int = Field(default=50, ge=0, le=200)
    top_k: int = Field(default=5, ge=3, le=10)

    owner: "User" = Relationship(back_populates="projects")

    documents: list["Document"] = Relationship(back_populates="project")

    chats: list["Chat"] = Relationship(back_populates="project")
