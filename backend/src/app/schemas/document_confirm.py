from uuid import UUID

from pydantic import BaseModel


class DocumentConfirmResponse(BaseModel):
    document_id: UUID
    filename: str
    status: str
    content_hash: str
    chunk_count: int