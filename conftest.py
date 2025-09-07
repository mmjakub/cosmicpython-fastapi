import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orm import mapper_registry


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
