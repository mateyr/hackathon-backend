from fastapi import Depends, HTTPException, status, Request
from casbin import AsyncEnforcer
from hackathon_backend.core.security import current_active_user
from hackathon_backend.models.user import User
from hackathon_backend.core.casbin.enforcer import enforcer


async def casbin_enforce(
    request: Request,
    enforcer=Depends(lambda: enforcer),
    user: User = Depends(current_active_user),
):
    sub = str(user.id)
    dom = str(getattr(user, "health_center_id", ""))
    path = request.url.path
    method = request.method

    if not enforcer.enforce(sub, dom, path, method):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
