from sqlalchemy import select

from backend.core.models import UserORM, UserRole
from backend.core.utils.password import hash_password
from backend.repositories.base import BaseRepository


class UserRepository(BaseRepository[UserORM]):
    model = UserORM
    pk = UserORM.user_id

    async def get_by_username(self, username: str) -> UserORM | None:
        return await self.session.scalar(
            select(UserORM).where(UserORM.user_name == username)
        )

    async def create_user(self, username: str, password: str, role: UserRole) -> UserORM:
        return await self.create(
            {
                "user_name": username,
                "password_hash": hash_password(password),
                "role": role,
            }
        )
