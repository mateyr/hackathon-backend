from typing import Optional
from casbin import AsyncEnforcer
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_403_FORBIDDEN
from starlette.types import ASGIApp, Receive, Scope, Send
from hackathon_backend.core.security import (
    current_active_user,
)


class CasbinMiddleware:
    """
    Middleware for Casbin enforcing based on JWT claims:
    - sub = user_id
    - dom = health_center_id
    Excludes specific endpoints like login.
    """

    def __init__(
        self,
        app: ASGIApp,
        enforcer: AsyncEnforcer,
        excluded_paths: Optional[list[str]] = None,
    ) -> None:
        self.app = app
        self.enforcer = enforcer
        self.excluded_paths = excluded_paths or [
            "/api/v1/auth/login",
            "/api/v1/auth/logout",
            "/docs",
            "/openapi.json",
        ]

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)

        if request.url.path in self.excluded_paths or request.method == "OPTIONS":
            await self.app(scope, receive, send)
            return

        try:
            user = await current_active_user(request)
            if user:
                sub = str(user.id)
                dom = str(getattr(user, "health_center_id", ""))
            else:
                sub = "anonymous"
                dom = ""
        except Exception:
            sub = "anonymous"
            dom = ""

        path = request.url.path
        method = request.method

        # Casbin enforce
        if self.enforcer.enforce(sub, dom, path, method):
            await self.app(scope, receive, send)
        else:
            response = JSONResponse(status_code=HTTP_403_FORBIDDEN, content="Forbidden")
            await response(scope, receive, send)
