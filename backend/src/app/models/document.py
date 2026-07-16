from typing import TYPE_CHECKING
from uuid import UUID
from sqlmodel import Field, Relationship
from app.models.base import BaseModel
from app.models.enums import DocumentStatus,MessageRole

if TYPE_CHECKING:
    from app.models.project import Project


class Document(BaseModel, table=True):
    __tablename__ = "documents"
    project_id: UUID = Field(
        foreign_key="projects.id",
        index=True,
    )
    filename: str
    content_hash: str = Field(index=True)
    status: DocumentStatus = Field(default=DocumentStatus.UPLOADING)
    role: MessageRole
    chunk_count: int = Field(default=0)
    project: "Project" = Relationship(back_populates="documents")
