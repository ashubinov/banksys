"""Зависимости FastAPI: сессия БД, сервисы, текущий пользователь и проверка ролей."""

from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import settings
from backend.core.exceptions import PermissionDeniedError
from backend.core.models import UserORM, UserRole, db_helper
from backend.repositories import (
    AccountRepository,
    ClientRepository,
    DepositRepository,
    UserRepository,
)
from backend.services import (
    AccountService,
    AuthService,
    ClientService,
    DepositService,
    UserService,
)

# --- БД ---------------------------------------------------------------------

SessionDep = Annotated[AsyncSession, Depends(db_helper.session_getter)]


# --- сервисы ----------------------------------------------------------------

def get_auth_service(session: SessionDep) -> AuthService:
    return AuthService(UserRepository(session))


def get_user_service(session: SessionDep) -> UserService:
    return UserService(UserRepository(session))


def get_deposit_service(session: SessionDep) -> DepositService:
    return DepositService(DepositRepository(session))


def get_client_service(session: SessionDep) -> ClientService:
    return ClientService(ClientRepository(session))


def get_account_service(session: SessionDep) -> AccountService:
    return AccountService(AccountRepository(session))


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
DepositServiceDep = Annotated[DepositService, Depends(get_deposit_service)]
ClientServiceDep = Annotated[ClientService, Depends(get_client_service)]
AccountServiceDep = Annotated[AccountService, Depends(get_account_service)]


# --- авторизация ------------------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.api.token_url)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserServiceDep,
) -> UserORM:
    return await user_service.get_by_token(token)


CurrentUserDep = Annotated[UserORM, Depends(get_current_user)]


def require_role(*allowed_roles: UserRole | str):
    allowed = {role.value if isinstance(role, UserRole) else role for role in allowed_roles}

    async def role_checker(current_user: CurrentUserDep) -> UserORM:
        if current_user.role not in allowed:
            raise PermissionDeniedError()
        return current_user

    return role_checker


AdminDep = Annotated[UserORM, Depends(require_role(UserRole.admin))]
OperatorDep = Annotated[
    UserORM, Depends(require_role(UserRole.bank_operator, UserRole.admin))
]
DepositManagerDep = Annotated[
    UserORM, Depends(require_role(UserRole.deposit_manager, UserRole.admin))
]
