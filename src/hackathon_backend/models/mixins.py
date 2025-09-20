from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


class TimestampMixin:
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )


class SoftDeleteMixin:
    deleted_at: datetime | None = Field(default=None)

    def soft_delete(self):
        self.deleted_at = datetime.now(timezone.utc)

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
