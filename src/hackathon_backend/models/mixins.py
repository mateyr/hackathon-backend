from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from sqlalchemy import event


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


@event.listens_for(SQLModel, "before_update", propagate=True)
def auto_update_timestamp(mapper, connection, target):
    if hasattr(target, "updated_at"):
        setattr(target, "updated_at", datetime.now(timezone.utc))
