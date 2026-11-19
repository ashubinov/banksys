from backend.repositories.client import ClientRepository
from backend.schemas.client import ClientSchema
from backend.services.base import BaseCrudService


class ClientService(BaseCrudService[ClientRepository, ClientSchema]):
    read_schema = ClientSchema
    not_found_message = "Client not found"
    delete_restricted_message = "Нельзя удалить данные клиента привязаны активные счета"
