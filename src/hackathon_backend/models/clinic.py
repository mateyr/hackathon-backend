from sqlmodel import Relationship, SQLModel, Field
from hackathon_backend.models.mixins import TimestampMixin, SoftDeleteMixin


# security.role table
class Clinic(SQLModel, TimestampMixin, SoftDeleteMixin, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, max_length=50)
    ruc_code: str = Field(nullable=False, unique=True, min_length=10, max_length=20, index=True)
    health_license: str = Field(nullable=False, unique=True, max_length=50, index=True)
    address: str = Field(nullable=False, max_length=50)
    phone: str = Field(nullable=False, max_length=20)

    user_clinic_roles: list["UserClinicRole"] = Relationship(
        back_populates="clinic",
    )

