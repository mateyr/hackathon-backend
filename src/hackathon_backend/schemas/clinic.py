from typing import List
from datetime import datetime
from sqlmodel import SQLModel
from pydantic import BaseModel

from hackathon_backend.schemas.role import RoleGet


class ClinicBase(SQLModel):
    name: str
    ruc_code: str
    health_license: str
    address: str
    phone: str


class ClinicCreate(ClinicBase):
    pass


class ClinicGet(ClinicBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None


class ClinicsResponse(SQLModel):
    clinics: List[ClinicGet] = []


class ClinicRole(BaseModel):
    id: int
    name: str
    roles: List[RoleGet] = []

    class Config:
        orm_mode = True
