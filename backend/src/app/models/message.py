from typing import TYPE_CHECKING
from uuid import UUID
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship
from app.models.base import BaseModel
if TYPE_CHECKING:
    from app.models.chat import Chat

class Message(BaseModel, table=True):
    __tablename__ = "messages"

    chat_id: UUID = Field(
        foreign_key="chats.id",
        index=True,
    )
    role: str
    content: str
    retrieval_snapshot: dict | None = Field(
        default=None,
        sa_column=Column(JSONB),
    )
    chat: "Chat" = Relationship(back_populates="messages")
