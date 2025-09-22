import asyncio
from pathlib import Path
from casbin import AsyncEnforcer
from casbin_async_sqlalchemy_adapter import Adapter
from hackathon_backend.core.config import settings

BASE_DIR = Path(__file__).resolve().parent
model_path = str(BASE_DIR / "model.conf")

adapter = Adapter(str(settings.SQLALCHEMY_DATABASE_URI))

enforcer = AsyncEnforcer(model_path, adapter)


async def create_casbin_rule():
    await adapter.create_table()
