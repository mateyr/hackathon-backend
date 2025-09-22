from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from hackathon_backend.core.casbin.enforcer import create_casbin_rule, enforcer
from hackathon_backend.core.config import settings
from hackathon_backend.api.main import api_router
from hackathon_backend.middlewares.fastapi_casbin_auth import CasbinMiddleware
from hackathon_backend.core.security import auth_backend, fastapi_users


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_casbin_rule()
    yield


app = FastAPI(
    title="hackathon_backend",
    openapi_url=f"/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
    swagger_ui_parameters={"docExpansion": "none"},
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["auth"],
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_middleware(CasbinMiddleware, enforcer=enforcer)

app.include_router(api_router, prefix=settings.API_V1_STR)
