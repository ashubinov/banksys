import jwt

from backend.core.exceptions import AlreadyExistsError, AuthenticationError
from backend.core.models import UserORM
from backend.core.utils.auth_utils import ACCESS_TOKEN, TOKEN_TYPE_FIELD, decode_jwt
from backend.repositories.user import UserRepository
from backend.schemas.user import UserCreateSchema, UserOutSchema


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repo = repository

    async def create_user(self, data: UserCreateSchema) -> UserOutSchema:
        if await self.repo.get_by_username(data.username):
            raise AlreadyExistsError("user_name already exists")
        user = await self.repo.create_user(data.username, data.password, data.role)
        return UserOutSchema.model_validate(user)

    async def get_all(self) -> list[UserOutSchema]:
        return [UserOutSchema.model_validate(u) for u in await self.repo.get_all()]

    async def get_by_token(self, token: str) -> UserORM:
        """Пользователь по access-токену. Бросает AuthenticationError."""
        try:
            payload = decode_jwt(token)
        except jwt.InvalidTokenError:
            raise AuthenticationError()

        username = payload.get("sub")
        if username is None or payload.get(TOKEN_TYPE_FIELD) != ACCESS_TOKEN:
            raise AuthenticationError()

        user = await self.repo.get_by_username(username)
        if user is None:
            raise AuthenticationError()
        return user
