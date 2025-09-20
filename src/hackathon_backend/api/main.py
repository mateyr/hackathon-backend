from fastapi import APIRouter
from hackathon_backend.api.routes import auth
from hackathon_backend.api.routes import users
from hackathon_backend.api.routes import me
from hackathon_backend.api.routes import roles
from hackathon_backend.api.routes import clinics

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(me.router)
api_router.include_router(roles.router)
api_router.include_router(clinics.router)
