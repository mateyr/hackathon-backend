from datetime import datetime, timezone
from sqlalchemy import Column, event, DateTime, text
from sqlmodel import DateTime, SQLModel, func
from sqlalchemy.orm import declared_attr


class CreatedAtMixin:
    @declared_attr
    def created_at(self):
        return Column(DateTime(timezone=True), server_default=func.now(), nullable=True)


class UpdatedAtMixin:
    @declared_attr
    def updated_at(self):
        return Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=True,
        )


class DeletedAtMixin:
    @declared_attr
    def deleted_at(self):
        return Column(
            DateTime(timezone=True),
            server_default=text("NULL"),
            default=None,
            index=True,
        )

    def soft_delete(self):
        self.deleted_at = func.now()

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None


class DTMixin(CreatedAtMixin, UpdatedAtMixin, DeletedAtMixin):
    pass
