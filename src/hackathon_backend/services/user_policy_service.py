from collections import defaultdict
from sqlmodel import select
from casbin_async_sqlalchemy_adapter import CasbinRule


class UserPolicyService:
    def __init__(self, session_maker):
        self.session_maker = session_maker

    async def get_user_health_center_with_roles(self, user_id: int):
        async with self.session_maker() as session:
            rows = await session.execute(
                select(CasbinRule).where(CasbinRule.v0 == str(user_id))
            )
            rules = rows.scalars().all()

            clinic_roles = defaultdict(list)
            for r in rules:
                clinic_roles[r.v2].append(r.v1)

            return dict(clinic_roles)
