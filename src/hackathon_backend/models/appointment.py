from datetime import datetime
from sqlmodel import SQLModel, Field
from .mixins import DTMixin


class AppointmentBase(SQLModel):

    id: int = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id", nullable=False)
    doctor_id: int = Field(foreign_key="doctor.id", nullable=False)
    health_center_id: int = Field(foreign_key="clinic.id", nullable=False)

    appointment_date: datetime = Field(nullable=False)
    status: str = Field(default="scheduled")  # scheduled, in_progress, completed
    observations: str | None = None


class Appointment(AppointmentBase, DTMixin, table=True):
    pass
