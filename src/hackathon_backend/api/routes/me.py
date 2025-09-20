from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from hackathon_backend.core.db import engine
from hackathon_backend.models.user import User
from hackathon_backend.models.user_clinic_role import UserClinicRole
from hackathon_backend.schemas.api_response import ApiResponse
from hackathon_backend.schemas.clinic import ClinicRole
from hackathon_backend.schemas.role import RoleGet
from hackathon_backend.schemas.user import (
    UserMe,
    UserMeResponse,
)
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/me", tags=["me"])


# Dependencia rápida para crear sesiones
def get_session():
    with Session(engine) as session:
        yield session

#  Task-pending - obtaining the user_id directly from the authenticated user's JWT token
@router.get("/{user_id}", response_model=ApiResponse[UserMeResponse])
def get_user_me(user_id: int, session: Session = Depends(get_session)):

    statement = (
        select(User)
        .where(User.id == user_id)
        .options(
            selectinload(User.user_clinic_roles).selectinload(UserClinicRole.role),
            selectinload(User.user_clinic_roles).selectinload(UserClinicRole.clinic),
        )
    )

    user = session.exec(statement).unique().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = UserMe.model_validate(user)
    clinics_dict: dict[int, ClinicRole] = {}

    for ucr in user.user_clinic_roles:
        if not ucr.clinic or not ucr.role:
            continue
        clinic_id = ucr.clinic.id
        if clinic_id not in clinics_dict:
            clinics_dict[clinic_id] = ClinicRole(
                id=ucr.clinic.id,
                name=ucr.clinic.name,
                roles=[]
            )
        clinics_dict[clinic_id].roles.append(RoleGet.model_validate(ucr.role))

    user_data.clinics = list(clinics_dict.values())

    return ApiResponse(
        success=True,
        data=UserMeResponse(user=user_data),
        message="Users fetched successfully",
    )
