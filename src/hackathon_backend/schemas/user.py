from typing import List
from datetime import datetime
from pydantic import EmailStr
from sqlmodel import SQLModel

from hackathon_backend.schemas.clinic import ClinicRole


class LoginResponse(SQLModel):
    access_token: str
    token_type: str


class UserBase(SQLModel):
    first_name: str
    middle_name: str
    last_name: str
    second_last_name: str
    email: EmailStr
    age: int


class UserCreate(UserBase):
    password: str


class UserGet(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None
    roles: List[str] | None = []


class UserResponse(SQLModel):
    user: UserGet


class UsersResponse(SQLModel):
    users: List[UserGet]


class UserMe(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    clinics: List[ClinicRole] = []


class UserMeResponse(SQLModel):
    user: UserMe
