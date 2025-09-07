import pytest
from sqlalchemy import text, select

from model import OrderLine


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
