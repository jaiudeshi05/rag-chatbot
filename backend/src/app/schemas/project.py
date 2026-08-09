from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    chunk_size: int = Field(default=500, ge=200, le=1000)
    chunk_overlap: int = Field(default=50, ge=0, le=200)
    top_k: int = Field(default=5, ge=3, le=10)


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    chunk_size: int | None = Field(default=None, ge=200, le=1000)
    chunk_overlap: int | None = Field(default=None, ge=0, le=200)
    top_k: int | None = Field(default=None, ge=3, le=10)


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    name: str
    chunk_size: int
    chunk_overlap: int
    top_k: int
    created_at: datetime
    updated_at: datetime