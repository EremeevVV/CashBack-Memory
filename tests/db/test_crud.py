from datetime import date
from typing import Any, ClassVar

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from cashback_memory.db import model
from cashback_memory.db.crud import Repository


class TestOwnerRepository:
    new_data:ClassVar[dict[str,Any]] = {'name': 'test'}
    updated_data:ClassVar[dict[str,Any]]  = {'name': 'updated'}

    @pytest_asyncio.fixture
    def repository(self, mock_session: AsyncSession) -> Repository:
        return Repository(model.Owner, mock_session)

    @pytest.mark.asyncio()
    async def test_get(self, repository: Repository) -> None:
        # arrange
        instance = await repository.create(self.new_data)

        # act
        result = await repository.get(instance.id)

        # assert
        assert result == instance

    @pytest.mark.asyncio()
    async def test_list(self, repository: Repository) -> None:
        # arrange
        instance = await repository.create(self.new_data)

        # act
        result = await repository.list()

        # assert
        assert len(result) > 1
        assert result[-1] == instance

    @pytest.mark.asyncio()
    async def test_create(self, repository: Repository) -> None:
        # act
        result = await repository.create(self.new_data)

        # assert
        key, value = next(iter(self.new_data.items()))
        assert getattr(result, key) == value

    @pytest.mark.asyncio()
    async def test_update(self, repository: Repository) -> None:
        # arrange
        instance = await repository.create(self.new_data)

        # act
        result = await repository.update(instance.id, self.updated_data)

        # assert
        key, value = next(iter(self.updated_data.items()))
        assert getattr(result, key) == value

    @pytest.mark.asyncio()
    async def test_delete(self, repository: Repository) -> None:
        # arrange
        instance = await repository.create(self.new_data)

        # act
        result = await repository.delete(instance.id)

        # assert
        assert result == instance


class TestCategoryRepository(TestOwnerRepository):
    new_data:ClassVar[dict[str,Any]]  = {'name': 'test', 'description': 'some useful'}
    updated_data:ClassVar[dict[str,Any]]  = {'name': 'updated'}

    @pytest_asyncio.fixture
    async def repository(self, mock_session: AsyncSession) -> Repository:
        return Repository(model.Category, mock_session)


class TestShopRepository(TestOwnerRepository):
    new_data:ClassVar[dict[str,Any]]  = {'name': 'test', 'category_id': 1}
    updated_data:ClassVar[dict[str,Any]]  = {'name': 'updated'}

    @pytest_asyncio.fixture
    async def repository(self, mock_session: AsyncSession) -> Repository:
        return Repository(model.Shop, mock_session)


class TestBankRepository(TestOwnerRepository):
    new_data:ClassVar[dict[str,Any]]  = {'name': 'test'}
    updated_data:ClassVar[dict[str,Any]]  = {'name': 'updated'}

    @pytest_asyncio.fixture
    async def repository(self, mock_session: AsyncSession) -> Repository:
        return Repository(model.Bank, mock_session)


class TestCardRepository(TestOwnerRepository):
    new_data:ClassVar[dict[str,Any]]  = {'name': 'test', 'memo_number': 1111, 'bank_id': 1, 'owner_id': 1}
    updated_data:ClassVar[dict[str,Any]]  = {'name': 'updated'}

    @pytest_asyncio.fixture
    async def repository(self, mock_session: AsyncSession) -> Repository:
        return Repository(model.Card, mock_session)


class TestPromotionRepository(TestOwnerRepository):
    new_data:ClassVar[dict[str,Any]]  = {'start_date': date(2024, 1, 1), 'end_date': date(2024, 2, 1),
                'percent': 5, 'card_id': 1, 'category_id': 1}
    updated_data:ClassVar[dict[str,Any]]  = {'percent': 10}

    @pytest_asyncio.fixture
    async def repository(self, mock_session: AsyncSession) -> Repository:
        return Repository(model.Promotion, mock_session)
