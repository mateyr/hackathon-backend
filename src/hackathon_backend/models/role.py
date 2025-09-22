from sqlmodel import Relationship, SQLModel, Field


# security.role table
class Role(SQLModel, table=True):
    __table_args__ = {"schema": "security"}

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True, min_length=1, max_length=25)
    description: str | None = Field(default=None, max_length=255)

    # user_clinic_roles: list["UserClinicRole"] = Relationship(
    #     back_populates="role",
    # )
