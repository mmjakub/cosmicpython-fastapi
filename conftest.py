from collections.abc import Callable

import pytest
from sqlalchemy import create_engine, CursorResult, text
from sqlalchemy.orm import sessionmaker

from orm import mapper_registry
from repository import SARepository


@pytest.fixture()
def engine():
    engine = create_engine("sqlite:///:memory:")
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture()
def session_factory(engine):
    return sessionmaker(engine)


@pytest.fixture()
def session(session_factory):
    with session_factory() as session:
        yield session


@pytest.fixture()
def run_sql(session) -> Callable[[str], CursorResult]:
    def f(stmt: str) -> CursorResult:
        return session.execute(text(stmt))

    return f


@pytest.fixture()
def repo(session):
    return SARepository(session)
