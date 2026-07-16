from typing import TYPE_CHECKING
from uuid import UUID
from sqlmodel import Field, Relationship
from app.models.base import BaseModel
if TYPE_CHECKING:
    from app.models.message import Message
    from app.models.project import Project

class Chat(BaseModel, table=True):
    __tablename__ = "chats"
    project_id: UUID = Field(
        foreign_key="projects.id",
        index=True,
    )
    title: str
    project: "Project" = Relationship(back_populates="chats")
    messages: list["Message"] = Relationship(back_populates="chat")
