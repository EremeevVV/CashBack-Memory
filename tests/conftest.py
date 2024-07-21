from collections.abc import Generator
from datetime import date

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from cashback_memory.db import model


def populate_db(session: Session) -> None:
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


@pytest.fixture(scope='session')
def in_memory_engine() -> Engine:
    return create_engine('sqlite:///:memory:')


@pytest.fixture(scope='session')
def mock_session(in_memory_engine) -> Generator[Session, None, None]:
    model.Base.metadata.create_all(in_memory_engine)
    session_maker = sessionmaker(bind=in_memory_engine, expire_on_commit=False)
    with session_maker() as session:
        populate_db(session)
        session.commit()
        yield session
