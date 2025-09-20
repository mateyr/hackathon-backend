from typing import Annotated, Generator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from hackathon_backend.core.config import settings
from hackathon_backend.core.db import engine


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]
