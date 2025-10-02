from fastapi import APIRouter, Security
from fastapi.security import (
    HTTPAuthorizationCredentials,
)
from hackathon_backend.core.db import engine
from hackathon_backend.core.deps import oauth2_scheme, SessionDep
from hackathon_backend.schemas.api_response import ApiResponse
from hackathon_backend.schemas.user import (
    UserMe,
    UserMeResponse,
)

router = APIRouter(prefix="/me", tags=["me"])


@router.get("/", response_model=ApiResponse[str])
async def get_user_me(
    session: SessionDep,
    credentials: HTTPAuthorizationCredentials = Security(oauth2_scheme),
):
    return ApiResponse(
        success=True,
        data="",
        message="Users fetched successfully",
    )
