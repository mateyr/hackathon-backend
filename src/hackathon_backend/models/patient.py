from datetime import date
from sqlmodel import SQLModel, Field
from .mixins import DTMixin

class PatientBase(SQLModel):

    id: int = Field(primary_key=True, foreign_key="user.id")
    date_of_birth: date = Field(nullable=False)
    gender: str = Field(max_length=10, nullable=False)  # M/F/Other
    address: str | None = Field(default=None, max_length=255)
    insurance_number: str | None = Field(default=None, max_length=50)
    phone: str | None = Field(default=None, max_length=10)


class Patient(PatientBase, DTMixin, table=True):
    pass
