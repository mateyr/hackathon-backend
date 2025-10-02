from sqlmodel import Relationship, SQLModel, Field
from .mixins import DTMixin


# security.role table
class HealthCenterBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, max_length=50)
    address: str = Field(nullable=False, max_length=50)
    ruc: str = Field(
        nullable=False, unique=True, min_length=10, max_length=20, index=True
    )
    license: str = Field(nullable=False, unique=True, max_length=50, index=True)
    phone: str = Field(nullable=False, max_length=20)

    # user_clinic_roles: list["UserClinicRole"] = Relationship(
    #     back_populates="clinic",
    # )


class HealthCenter(HealthCenterBase, DTMixin, table=True):
    pass