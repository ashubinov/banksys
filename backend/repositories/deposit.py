from backend.core.models import DepositORM
from backend.repositories.base import BaseRepository


class DepositRepository(BaseRepository[DepositORM]):
    model = DepositORM
    pk = DepositORM.deposit_id
