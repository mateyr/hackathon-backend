from sqlmodel import create_engine
from hackathon_backend.core.config import settings


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
