from typing import Any, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cashback_memory.db.model import Base


class Repository:
    def __init__(self, model: Type[Base], session: AsyncSession) -> None:
        self.session = session
        self.model = model

    async def get(self, identity: int) -> Base:
        return await self.session.scalar(select(self.model).filter_by(id=identity))

    async def list(self) -> list[Base]:
        scalars = await self.session.scalars(select(self.model))
        return list(scalars)

    async def create(self, data: dict[str, Any]) -> Base:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.commit()
        return instance

    async def update(self, identity: int, data: dict[str, Any]) -> Base:
        instance = await self.get(identity)
        for key, value in data.items():
            setattr(instance, key, value)
        await self.session.commit()
        return instance

    async def delete(self, identity: int) -> Base:
        instance = await self.get(identity)
        await self.session.delete(instance)
        await self.session.commit()
        return instance
