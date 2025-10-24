from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import (
    HTTPAuthorizationCredentials,
)
from hackathon_backend.core.db import engine
from hackathon_backend.core.deps import oauth2_scheme, SessionDep
from hackathon_backend.middlewares.fastapi_casbin_auth import casbin_enforce
from hackathon_backend.models.user import User
from hackathon_backend.schemas.api_response import ApiResponse
from hackathon_backend.schemas.user import (
    UserMeResponse,
)
from hackathon_backend.core.security import current_active_user

router = APIRouter(prefix="/me", tags=["me"])


@router.get("/", response_model=ApiResponse[str])
async def get_user_me(user: User = Depends(current_active_user)):
    return ApiResponse(
        success=True,
        data="",
        message="Users fetched successfully",
    )
