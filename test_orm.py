from datetime import date

from sqlalchemy import text, select

from model import OrderLine, Batch


def test_can_load_order_lines(session):
    expected = [
        OrderLine("ord-01", "LED-TORCH", 5),
        OrderLine("ord-02", "BIG-RED-BUTTON", 7),
    ]
    session.execute(
        text(
            "INSERT INTO order_line (order_id, sku, quantity) VALUES "
            "('ord-01', 'LED-TORCH', 5),"
            "('ord-02', 'BIG-RED-BUTTON', 7)"
        )
    )

    lines = session.scalars(select(OrderLine)).all()

    assert lines == expected


def test_can_store_order_lines(session):
    rows = [("ord-01", "LED-TORCH", 5), ("ord-02", "BIG-RED-BUTTON", 7)]
    lines = [OrderLine(*row) for row in rows]
    select_all_lines = text("SELECT order_id, sku, quantity FROM order_line")

    for line in lines:
        session.add(line)
    session.commit()

    assert session.execute(select_all_lines).all() == rows


def test_loading_batches(session):
    eta = date.today()
    expected = [
        Batch("ba-01", "FOO-GIZMO", 42, None),
        Batch("ba-02", "BAR-BAZ", 22, eta),
    ]
    session.execute(
        text(
            f"INSERT INTO batch (ref, sku, qty, eta) VALUES"
            f'("ba-01", "FOO-GIZMO", 42, null), ("ba-02", "BAR-BAZ", 22, "{eta}")'
        )
    )

    batches = session.scalars(select(Batch)).all()

    assert batches == expected


def test_saving_batches(session):
    eta = date.today()
    rows = [
        ("ba-01", "FOO-GIZMO", 42, None),
        ("ba-02", "BAR-BAZ", 22, eta.isoformat()),
    ]

    for row in rows:
        session.add(
            Batch(
                *row[:-1], date.fromisoformat(row[-1]) if row[-1] is not None else None
            )
        )
    session.commit()

    assert session.execute(text("SELECT ref, sku, qty, eta FROM batch")).all() == rows


def test_loading_allocations(session):
    lines_sql = "INSERT INTO order_line (order_id, sku, quantity) VALUES ('o1','foo-bar', 1), ('o2', 'foo-bar', 2)"
    batch_sql = (
        "INSERT INTO batch (ref, sku, qty, eta) VALUES ('b1', 'foo-bar', 5, null)"
    )
    allocation_sql = (
        "INSERT INTO allocation (order_line_id, batch_id) VALUES (1, 1), (2, 1)"
    )
    for stmt in (lines_sql, batch_sql, allocation_sql):
        session.execute(text(stmt))

    batch = session.scalars(select(Batch)).one()

    assert batch._allocations == {
        OrderLine("o1", "foo-bar", 1),
        OrderLine("o2", "foo-bar", 2),
    }


def test_saving_allocations(session):
    batch = Batch("b1", "foo-bar", 123, None)
    batch.allocate(OrderLine("o1", "foo-bar", 12))
    batch.allocate(OrderLine("o2", "foo-bar", 21))

    session.add(batch)
    session.commit()

    assert list(
        session.execute(text("SELECT order_line_id, batch_id FROM allocation"))
    ) == [(1, 1), (2, 1)]
