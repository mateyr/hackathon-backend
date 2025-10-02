from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from hackathon_backend.core.config import settings
from hackathon_backend.core.db import get_async_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
