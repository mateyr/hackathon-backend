from fastapi_users.authentication import JWTStrategy
from fastapi_users.jwt import generate_jwt
from hackathon_backend.models.user import User


# Custom JWT strategy that includes the user's selected health center and role
# in the token if the user has only one option; otherwise sets them to None.
class CustomJWTStrategy(JWTStrategy):
    def __init__(self, user_policy_service, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_policy_service = user_policy_service

    async def write_token(self, user: User) -> str:
        health_center_roles = (
            await self.user_policy_service.get_user_health_center_with_roles(user.id)
        )

        has_single_health_center = len(health_center_roles) == 1
        health_center_id = None
        role_id = None

        if has_single_health_center:
            hc_id = list(health_center_roles.keys())[0]
            roles_in_hc = health_center_roles[hc_id]
            health_center_id = hc_id
            if len(roles_in_hc) == 1:
                role_id = roles_in_hc[0]
            else:
                role_id = None
        else:
            health_center_id = None
            role_id = None

        data = {
            "user_id": str(user.id),
            "aud": self.token_audience,
            "health_center_id": health_center_id,
            "role_id": role_id,
        }

        return generate_jwt(
            data, self.encode_key, self.lifetime_seconds, algorithm=self.algorithm
        )
