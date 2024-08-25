import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from cashback_memory.db.crud import Repository
from cashback_memory.db.model import Owner


class TestOwnerRepository:
    @pytest_asyncio.fixture
    def repository(self, mock_session: AsyncSession) -> Repository:
        return Repository(Owner, mock_session)

    @pytest.mark.asyncio()
    async def test_get(self, repository: Repository) -> None:
        # arrange
        data = {'name': 'test'}
        instance = await repository.create(data)

        # act
        result = await repository.get(instance.id)

        # assert
        assert result == instance

    @pytest.mark.asyncio()
    async def test_list(self, repository: Repository) -> None:
        # arrange
        data = {'name': 'test'}
        instance = await repository.create(data)

        # act
        result = await repository.list()

        # assert
        assert len(result) > 1
        assert result[-1] == instance

    @pytest.mark.asyncio()
    async def test_create(self, repository: Repository) -> None:
        # arrange
        data = {'name': 'test'}

        # act
        result = await repository.create(data)

        # assert
        assert result.name == data['name']

    @pytest.mark.asyncio()
    async def test_update(self, repository: Repository) -> None:
        # arrange
        data = {'name': 'test'}
        instance = await repository.create(data)
        updated_data = {'name': 'updated'}

        # act
        result = await repository.update(instance.id, updated_data)

        # assert
        assert result.name == updated_data['name']

    @pytest.mark.asyncio()
    async def test_delete(self, repository: Repository) -> None:
        # arrange
        data = {'name': 'test'}
        instance = await repository.create(data)

        # act
        result = await repository.delete(instance.id)

        # assert
        assert result == instance
