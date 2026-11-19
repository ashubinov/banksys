from backend.core.models import AccountORM
from backend.repositories.base import BaseRepository


class AccountRepository(BaseRepository[AccountORM]):
    model = AccountORM
    pk = AccountORM.account_numb
