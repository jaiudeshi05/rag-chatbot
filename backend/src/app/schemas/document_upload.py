from uuid import UUID

from pydantic import BaseModel, Field


class DocumentUploadUrlRequest(BaseModel):
    filename: str = Field(
        min_length=1,
        max_length=255,
    )

    content_type: str = Field(
        min_length=1,
        max_length=255,
    )


class DocumentUploadUrlResponse(BaseModel):
    document_id: UUID
    upload_url: str
    object_key: str