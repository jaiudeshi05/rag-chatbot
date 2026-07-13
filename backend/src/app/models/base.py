from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class BaseUUIDModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)


class TimestampModel(SQLModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class BaseModel(BaseUUIDModel, TimestampModel):
    pass