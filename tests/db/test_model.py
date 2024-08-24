import pytest
from sqlalchemy import select

from cashback_memory.db import model


@pytest.mark.asyncio
async def test_init_db(mock_session) -> None:
    stm = select(model.Promotion)
    promos = await mock_session.scalars(stm)
    promos = promos.all()
    expected_len = 4
    expected_last_percent = 100
    assert expected_len == len(promos)
    assert expected_last_percent == promos[-1].percent
