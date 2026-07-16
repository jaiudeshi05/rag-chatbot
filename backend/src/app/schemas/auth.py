from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GoogleUserInfo(BaseModel):
    sub: str
    email: str
    name: str
    picture: str | None = None
    email_verified: bool = False


class AuthenticatedUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    name: str
    profile_picture: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
