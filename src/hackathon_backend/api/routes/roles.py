from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from hackathon_backend.casbin.enforcer import check_permission
from hackathon_backend.core.db import engine
from hackathon_backend.models.role import Role
from hackathon_backend.schemas.api_response import ApiResponse
from hackathon_backend.schemas.role import RoleGet, RolesResponse  # define estos schemas

router = APIRouter(prefix="/roles", tags=["roles"])

def get_session():
    with Session(engine) as session:
        yield session


@router.get("/", response_model=ApiResponse[RolesResponse])
def read_roles(session: Session = Depends(get_session)) -> ApiResponse[RolesResponse]:
    #check_permission(user_role, "/roles", "GET")
    statement = select(Role)
    roles = session.exec(statement).all()
    roles_data: list[RoleGet] = [RoleGet.model_validate(r) for r in roles]

    return ApiResponse(
        success=True,
        data=RolesResponse(roles=roles_data),
        message="Roles fetched successfully",
    )
