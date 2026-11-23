from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from backend.core.exceptions import NotFoundError, RelatedObjectsError
from backend.repositories.base import BaseRepository

RepoT = TypeVar("RepoT", bound=BaseRepository)
SchemaT = TypeVar("SchemaT", bound=BaseModel)


class BaseCrudService(Generic[RepoT, SchemaT]):
    """Общая бизнес-логика CRUD: проверки существования и перевод
    ошибок БД в ошибки приложения (core.exceptions)."""

    read_schema: type[SchemaT]
    not_found_message: str = "Not found"
    delete_restricted_message: str = "Object has related records"

    def __init__(self, repository: RepoT) -> None:
        self.repo = repository

    async def get(self, obj_id: int) -> SchemaT:
        obj = await self.repo.get_by_id(obj_id)
        if obj is None:
            raise NotFoundError(self.not_found_message)
        return self.read_schema.model_validate(obj)

    async def get_all(self) -> list[SchemaT]:
        return [self.read_schema.model_validate(obj) for obj in await self.repo.get_all()]

    async def create(self, data: BaseModel) -> SchemaT:
        obj = await self.repo.create(data.model_dump())
        return self.read_schema.model_validate(obj)

    async def update(self, obj_id: int, data: BaseModel) -> SchemaT:
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            # нечего обновлять — просто возвращаем текущую запись (или 404)
            return await self.get(obj_id)

        obj = await self.repo.update(obj_id, update_data)
        if obj is None:
            raise NotFoundError(self.not_found_message)
        return self.read_schema.model_validate(obj)

    async def delete(self, obj_id: int) -> None:
        try:
            deleted = await self.repo.delete(obj_id)
        except IntegrityError:
            raise RelatedObjectsError(self.delete_restricted_message)
        if not deleted:
            raise NotFoundError(self.not_found_message)
