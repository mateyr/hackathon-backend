from datetime import timedelta
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase


from hackathon_backend.core.db import async_session, get_user_db
from hackathon_backend.core.fastapi_users.custom_authentication_backend import CustomAuthenticationBackend
from hackathon_backend.models.user import User
from hackathon_backend.core.config import settings
from hackathon_backend.core.fastapi_users.custom_jwt_strategy import CustomJWTStrategy
from hackathon_backend.services import user_policy_service


class UserManager(BaseUserManager[User, int]):
    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/login")

access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

user_policy_service_instance = user_policy_service.UserPolicyService(
    session_maker=async_session
)


def get_jwt_strategy() -> CustomJWTStrategy:
    return CustomJWTStrategy(
        secret=settings.SECRET_KEY,
        lifetime_seconds=int(access_token_expires.total_seconds()),
        user_policy_service=user_policy_service_instance,
    )


auth_backend = CustomAuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
