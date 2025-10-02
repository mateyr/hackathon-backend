from datetime import datetime
from sqlmodel import SQLModel


class AppointmentBase(SQLModel):
    patient_id: int
    doctor_id: int
    health_center_id: int
    appointment_date: datetime
    status: str = "scheduled"  
    observations: str | None = None

    


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentGet(AppointmentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None


class AppointmentUpdate(SQLModel):
    patient_id: int | None = None
    doctor_id: int | None = None
    health_center_id: int | None = None
    appointment_date: datetime | None = None
    status: str | None = None
    observations: str | None = None



class AppointmentsResponse(SQLModel):
    roles: list[AppointmentGet] = [] 