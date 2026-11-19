from backend.core.models import ClientORM
from backend.repositories.base import BaseRepository


class ClientRepository(BaseRepository[ClientORM]):
    model = ClientORM
    pk = ClientORM.client_id
