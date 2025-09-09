import os
from functools import cache

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import model
import repository

app = FastAPI()


def get_postgres_url():
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", 5432)
    database = os.getenv("POSTGRES_DATABASE", "postgres")
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


@cache
def get_session_factory():
    # TODO: add explicit starting of mappers
    import orm

    return sessionmaker(create_engine(get_postgres_url()))


@app.post("/allocate")
def allocate(line: model.OrderLine):
    session_factory = get_session_factory()
    try:
        with session_factory() as session, session.begin():
            repo = repository.SARepository(session)
            batches = repo.get_all()
            ref = model.allocate(line, batches)
            return {"batch_ref": ref}
    except model.OutOfStock as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
