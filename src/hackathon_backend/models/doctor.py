from sqlmodel import Field, SQLModel
from hackathon_backend.models.mixins import DTMixin


class DoctorBase(SQLModel):

    id: int = Field(primary_key=True, foreign_key="user.id")
    specialization: str = Field(max_length=100, nullable=False)
    license_number: str = Field(unique=True, max_length=50, nullable=False)
    years_experience: str | None = Field(default=None, ge=0)
    phone: str | None = Field(default=None, max_length=20)


class Doctor(DoctorBase, DTMixin, table=True):
    pass