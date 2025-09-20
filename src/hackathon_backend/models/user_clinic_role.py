from sqlmodel import Relationship, SQLModel, Field
from hackathon_backend.models.mixins import TimestampMixin, SoftDeleteMixin
from hackathon_backend.models.user import User
from hackathon_backend.models.clinic import Clinic
from hackathon_backend.models.role import Role


class UserClinicRole(SQLModel, TimestampMixin, SoftDeleteMixin, table=True):
    __tablename__ = "user_clinic_role"
    __table_args__ = {"schema": "security"}

    user_id: int | None = Field(foreign_key="user.id", primary_key=True)
    role_id: int | None = Field(foreign_key="security.role.id", primary_key=True)
    clinic_id: int | None = Field(foreign_key="clinic.id", primary_key=True)

    user: User | None = Relationship(back_populates="user_clinic_roles")
    role: Role | None = Relationship(back_populates="user_clinic_roles")
    clinic: Clinic | None = Relationship(back_populates="user_clinic_roles")
