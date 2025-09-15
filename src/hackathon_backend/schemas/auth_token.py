from sqlmodel import SQLModel


class AuthToken(SQLModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
