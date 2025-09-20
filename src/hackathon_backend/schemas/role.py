from datetime import datetime
from typing import List
from sqlmodel import SQLModel
from enum import Enum


# Enum for available roles
class RoleName(str, Enum):
    ADMINISTRADOR = "administrador"
    PATIENT = "patient"
    DOCTOR = "doctor"
    CLINIC_ADMINISTRATOR = "clinic_administrator"


class RoleBase(SQLModel):
    name: RoleName
    description: str | None = None


class RoleCreate(RoleBase):
    pass


class RoleGet(RoleBase):
    id: int
    deleted_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class RolesResponse(SQLModel):
    roles: List[RoleGet] = []
