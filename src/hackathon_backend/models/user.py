from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    middle_name: str | None
    last_name: str
    second_last_name: str | None
    email: EmailStr
    age: int
    hashed_password: str
    is_active: bool = True
