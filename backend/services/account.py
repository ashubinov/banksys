from backend.repositories.account import AccountRepository
from backend.schemas.account import AccountShema
from backend.services.base import BaseCrudService


class AccountService(BaseCrudService[AccountRepository, AccountShema]):
    read_schema = AccountShema
    not_found_message = "Account not found"
    delete_restricted_message = "Нельзя удалить счёт: на него ссылаются другие данные"
