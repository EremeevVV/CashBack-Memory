from collections.abc import Generator
from datetime import date

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from cashback_memory.db import model
import pytest_asyncio


# @event.listens_for(AsyncEngine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record) -> None:
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()


async def populate_db(session: AsyncSession) -> None:
    session.add_all([
        model.Category(name='Рестораны', description='Там кормят и должны быть официанты'),
        model.Category(name='Одежда и обувь', description='Магазины, где продают трусы, носки, сандали и т.д.'),
        model.Category(name='3 мороженных в Шестерочке',
                       description='Только три мороженных в стаканчике, без шоколада', special=True),
        model.Shop(name='Царский пельмень', category_id=1), model.Shop(name='Мир шнурков', category_id=2),
        model.Owner(name='Виктор'), model.Owner(name='Снежана'),
        model.Bank(name='Ва-банк'), model.Bank(name='Огр банк'),
        model.Card(name='Бабки бэк. Силвер', memo_number=1234, bank_id=1, owner_id=1),
        model.Card(name='Кредит не спит. Платинум', memo_number=4532, bank_id=2, owner_id=2),
        model.Card(name='Бабки бэк. Золотой.', memo_number=8954, bank_id=1, owner_id=2),
        model.Card(name='Сертаки', memo_number=5632, bank_id=1, owner_id=2),
        model.Promotion(start_date=date(2024, 1, 1),
                        end_date=date(2024, 2, 1), percent=3, card_id=1, category_id=1),
        model.Promotion(start_date=date(2024, 1, 1),
                        end_date=date(2024, 2, 1), percent=5, card_id=1, category_id=2),
        model.Promotion(start_date=date(2024, 2, 1),
                        end_date=date(2024, 3, 1), percent=10, card_id=3, category_id=2),
        model.Promotion(start_date=date(2024, 2, 1),
                        end_date=date(2024, 2, 3), percent=100, card_id=4, category_id=3),
    ])
    await session.commit()


@pytest.fixture(scope='session')
def in_memory_engine() -> AsyncEngine:
    return create_async_engine('sqlite+aiosqlite:///:memory:')


@pytest_asyncio.fixture
async def mock_session(in_memory_engine) -> Generator[AsyncSession, None, None]:
    session_maker = async_sessionmaker(bind=in_memory_engine, expire_on_commit=False)
    await create_tables(in_memory_engine)
    async with session_maker() as session:
        await populate_db(session)
        await session.commit()
        yield session
    await drop_tables(in_memory_engine)


async def create_tables(in_memory_engine:AsyncEngine) -> None:
    async with in_memory_engine.begin() as conn:
        await conn.run_sync(model.Base.metadata.create_all)


async def drop_tables(in_memory_engine:AsyncEngine) -> None:
    async with in_memory_engine.begin() as conn:
        await conn.run_sync(model.Base.metadata.drop_all)
