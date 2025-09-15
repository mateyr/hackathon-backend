from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from hackathon_backend.core.deps import SessionDep
from hackathon_backend.core.config import settings
from hackathon_backend.core import security
from hackathon_backend.schemas.api_response import ApiResponse
from hackathon_backend.services import auth
from hackathon_backend.schemas.auth_token import AuthToken


router = APIRouter(tags=["auth"])


@router.post("/login", response_model=ApiResponse[AuthToken])
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> ApiResponse[AuthToken]:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = auth.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    auth_token = AuthToken(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        expires_in=int(access_token_expires.total_seconds()),
    )
    return ApiResponse(
        success=True,
        data=auth_token,
        message="Login successful",
    )
