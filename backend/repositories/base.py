from typing import Any, Generic, Sequence, TypeVar

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from backend.core.models import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """Общие CRUD-операции. Наследник задаёт модель и её первичный ключ."""

    model: type[ModelT]
    pk: InstrumentedAttribute

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, obj_id: int) -> ModelT | None:
        return await self.session.scalar(select(self.model).where(self.pk == obj_id))

    async def get_all(self) -> Sequence[ModelT]:
        result = await self.session.execute(select(self.model).order_by(self.pk))
        return result.scalars().all()

    async def count(self) -> int:
        return await self.session.scalar(select(func.count()).select_from(self.model)) or 0

    async def create(self, data: dict[str, Any]) -> ModelT:
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def bulk_create(self, rows: list[dict[str, Any]]) -> None:
        await self.session.execute(insert(self.model).values(rows))
        await self.session.commit()

    async def update(self, obj_id: int, data: dict[str, Any]) -> ModelT | None:
        query = (
            update(self.model)
            .where(self.pk == obj_id)
            .values(data)
            .returning(self.model)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def delete(self, obj_id: int) -> bool:
        """Возвращает False, если записи нет.
        Бросает IntegrityError, если на запись ссылаются другие таблицы."""
        try:
            result = await self.session.execute(delete(self.model).where(self.pk == obj_id))
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise
        return result.rowcount > 0
