from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import settings
from backend.core.models import UserRole
from backend.core.utils.initial_data import ACCOUNTS, CLIENTS, DEPOSITS
from backend.repositories import (
    AccountRepository,
    ClientRepository,
    DepositRepository,
    UserRepository,
)


class SeedService:
    """Заполнение БД стартовыми данными при запуске приложения.
    Повторный запуск ничего не дублирует."""

    def __init__(self, session: AsyncSession) -> None:
        self.deposits = DepositRepository(session)
        self.clients = ClientRepository(session)
        self.accounts = AccountRepository(session)
        self.users = UserRepository(session)

    async def seed_demo_data(self) -> None:
        if await self.deposits.count() or await self.clients.count():
            return
        await self.deposits.bulk_create(DEPOSITS)
        await self.clients.bulk_create(CLIENTS)
        await self.accounts.bulk_create(ACCOUNTS)

    async def ensure_admin(self) -> None:
        if await self.users.get_by_username(settings.admin_first_username):
            return
        await self.users.create_user(
            username=settings.admin_first_username,
            password=settings.admin_first_password,
            role=UserRole.admin,
        )

    async def run(self) -> None:
        await self.seed_demo_data()
        await self.ensure_admin()
