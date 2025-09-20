from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from hackathon_backend.core.db import engine
from hackathon_backend.models.user import User
from hackathon_backend.models.user_clinic_role import UserClinicRole
from hackathon_backend.schemas.api_response import ApiResponse
from hackathon_backend.schemas.user import UserGet, UsersResponse
from sqlalchemy.orm import selectinload


router = APIRouter(prefix="/users", tags=["users"])


# Dependencia rápida para crear sesiones
def get_session():
    with Session(engine) as session:
        yield session


@router.get("/", response_model=ApiResponse[UsersResponse])
def read_users_test(
    session: Session = Depends(get_session),
) -> ApiResponse[UsersResponse]:
    
    statement = select(User).options(
        selectinload(User.user_clinic_roles).selectinload(UserClinicRole.role)
    )
    users = session.exec(statement).all()

    if not users:
        raise HTTPException(status_code=404, detail="Users not found")

    users_data: List[UserGet] = [
        UserGet.model_validate(
            user,
            update={
                "roles": [ucr.role.name for ucr in user.user_clinic_roles if ucr.role]
            },
        )
        for user in users
    ]

    return ApiResponse(
        success=True,
        data=UsersResponse(users=users_data),
        message="Users fetched successfully",
    )
