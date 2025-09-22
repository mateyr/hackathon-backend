from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from hackathon_backend.models.mixins import DTMixin


# For Columns Order
class UserBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str = Field(min_length=1, max_length=50)
    middle_name: str | None = Field(default=None, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    second_last_name: str | None = Field(default=None, max_length=50)
    email: EmailStr = Field(index=True, unique=True)
    age: int = Field(ge=0, le=120)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)


class User(DTMixin, UserBase, table=True):
    # user_clinic_roles: list["UserClinicRole"] = Relationship(
    #     back_populates="user",
    # )
    pass
