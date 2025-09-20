from sqlmodel import Relationship, SQLModel, Field
from hackathon_backend.models.mixins import TimestampMixin, SoftDeleteMixin

# security.role table
class Role(SQLModel, TimestampMixin, SoftDeleteMixin, table=True):
    __table_args__ = {"schema": "security"}

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True, min_length=1, max_length=25)
    description: str | None = Field(default=None, max_length=255)

    user_clinic_roles: list["UserClinicRole"] = Relationship(
        back_populates="role",
    )
