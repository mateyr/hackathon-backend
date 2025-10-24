from fastapi import APIRouter, Depends
from hackathon_backend.api.routes import users
from hackathon_backend.api.routes import me
from hackathon_backend.middlewares.fastapi_casbin_auth import casbin_enforce

api_router = APIRouter(dependencies=[Depends(casbin_enforce)])

api_router.include_router(me.router)
api_router.include_router(users.router)
