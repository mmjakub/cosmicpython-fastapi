from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from model import Batch


class BaseRepository(ABC):
    @abstractmethod
    def add(self, batch: Batch) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, ref: str) -> Batch:
        raise NotImplementedError


class SARepository(BaseRepository):

    def __init__(self, session: Session):
        self.session = session

    def add(self, batch: Batch) -> None:
        self.session.add(batch)

    def get(self, ref: str) -> Batch:
        try:
            return self.session.scalars(select(Batch).where(Batch.ref == ref)).one()
        except NoResultFound:
            raise BatchNotFound(f"No Batch with ref={ref}")


class BatchNotFound(Exception):
    pass
