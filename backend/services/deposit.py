from backend.repositories.deposit import DepositRepository
from backend.schemas.deposit import DepositShema
from backend.services.base import BaseCrudService


class DepositService(BaseCrudService[DepositRepository, DepositShema]):
    read_schema = DepositShema
    not_found_message = "Deposit not found"
    delete_restricted_message = "Нельзя удалить депозит привязаны активные счета"
