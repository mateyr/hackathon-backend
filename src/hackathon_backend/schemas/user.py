from typing import List
from pydantic import EmailStr
from sqlmodel import SQLModel


class UserGet(SQLModel):
    id: int
    first_name: str
    middle_name: str
    last_nameL: str
    second_last_name: str
    email: EmailStr
    age: int
    is_active: bool


class UsersResponse(SQLModel):
    users: List[UserGet]
