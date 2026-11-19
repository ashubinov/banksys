from pydantic import BaseModel, ConfigDict

from backend.core.models.models import UserRole


class UserCreateSchema(BaseModel):
    username: str
    password: str
    role: UserRole


class LoginRequestSchema(BaseModel):
    username: str
    password: str


class UserOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    user_name: str
    role: UserRole


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class TokenData(BaseModel):
    username: str
