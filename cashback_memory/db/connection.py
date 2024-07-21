from collections.abc import Generator

from sqlalchemy import Session, create_engine, session_maker


engine = create_engine("sqlite://var/local.db", echo=True)


def get_connection() -> Generator[Session, None, None]:
    with session_maker(engine) as session:
        yield session
