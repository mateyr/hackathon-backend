from fastapi.responses import JSONResponse
from fastapi_users.authentication import AuthenticationBackend
from fastapi_users.authentication.strategy import Strategy
from hackathon_backend.models.user import User
from hackathon_backend.schemas.api_response import ApiResponse
from hackathon_backend.schemas.user import LoginResponse


class CustomAuthenticationBackend(AuthenticationBackend):
    async def login(self, strategy: Strategy[User, int], user: User) -> JSONResponse:
        token = await strategy.write_token(user)

        api_response = ApiResponse[LoginResponse](
            success=True,
            data=LoginResponse(
                access_token=token,
                token_type="bearer",
            ),
            message="Login successful",
        )
        return JSONResponse(content=api_response.model_dump())
