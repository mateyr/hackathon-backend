from fastapi import APIRouter
from hackathon_backend.api.routes import users
from hackathon_backend.api.routes import me

api_router = APIRouter()

api_router.include_router(me.router)
api_router.include_router(users.router)
