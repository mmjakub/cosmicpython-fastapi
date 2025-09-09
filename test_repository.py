import pytest
from sqlalchemy import text

from model import Batch, OrderLine
from repository import BatchNotFound


def test_can_save_a_batch(session, repo):
    row = ("b1", "sku1", 23, None)

    repo.add(Batch(*row))
    session.commit()

    assert session.execute(text("SELECT ref, sku, qty, eta FROM batch")).all() == [row]


def test_can_load_a_batch(repo, run_sql):
    run_sql("INSERT INTO batch (ref, sku, qty, eta) VALUES ('b1', 'sku1', 12, null)")

    batch = repo.get("b1")

    assert batch.ref == "b1"
    assert batch.sku == "sku1"
    assert batch._base_quantity == 12
    assert batch.eta is None


def test_raises_exception_when_no_batch_is_found(repo):

    with pytest.raises(BatchNotFound) as exc_info:
        repo.get("b1")

    assert "b1" in str(exc_info.value)


def test_can_store_a_modified_batch(repo, run_sql, session):
    run_sql("INSERT INTO batch (ref, sku, qty, eta) VALUES ('b1', 'sku1', 12, null)")
    batch = repo.get("b1")

    batch._base_quantity -= 3
    repo.add(batch)
    session.commit()

    assert run_sql("SELECT ref, sku, qty, eta FROM batch").all() == [
        ("b1", "sku1", 9, None)
    ]


def test_can_load_a_batch_with_allocations(repo, run_sql):
    run_sql(
        "INSERT INTO order_line (order_id, sku, quantity) VALUES ('o1','foo-bar', 5), ('o2', 'foo-bar', 7)"
    )
    run_sql("INSERT INTO batch (ref, sku, qty, eta) VALUES ('b1', 'foo-bar', 33, null)")
    run_sql("INSERT INTO allocation (order_line_id, batch_id) VALUES (1, 1), (2, 1)")

    batch = repo.get("b1")

    assert batch._allocations == {
        OrderLine("o1", "foo-bar", 5),
        OrderLine("o2", "foo-bar", 7),
    }
