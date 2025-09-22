from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from hackathon_backend.core.db import engine
from hackathon_backend.models.user import User
from hackathon_backend.schemas.api_response import ApiResponse
from hackathon_backend.schemas.user import UserGet, UsersResponse


router = APIRouter(prefix="/users", tags=["users"])


# Dependencia rápida para crear sesiones
def get_session():
    with Session(engine) as session:
        yield session


@router.get("/", response_model=ApiResponse[UsersResponse])
def read_users_test(
    session: Session = Depends(get_session),
) -> ApiResponse[UsersResponse]:
    """
    Example endpoint: Retrieve all users.
    """
    statement = select(User)
    users = session.exec(statement).all()
    users_data = [UserGet.model_validate(u) for u in users]

    return ApiResponse(
        success=True,
        data=UsersResponse(users=users_data),
        message="Users fetched successfully",
    )
