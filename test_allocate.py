from datetime import date, timedelta

import pytest

from model import allocate, Batch, OrderLine, OutOfStock
from test_batch import make_batch_and_line

tomorrow = date.today() + timedelta(days=1)
in_two_days = date.today() + timedelta(days=2)
in_a_fortnight = date.today() + timedelta(days=14)


def test_prefers_warehouse_stock_to_transit():
    warehouse_batch = Batch("wh-batch-01", "PORTABLE-SWING-SET", 10, None)
    shipment_batch = Batch("shp-batch-01", "PORTABLE-SWING-SET", 10, in_a_fortnight)
    line = OrderLine("ord-01", "PORTABLE-SWING-SET", 5)

    allocate(line, [shipment_batch, warehouse_batch])

    assert shipment_batch.available_quantity == 10
    assert warehouse_batch.available_quantity == 5


def test_prefers_earliest_batch():
    early_batch = Batch("shp-batch-01", "CEILING-FAN", 10, tomorrow)
    medium_batch = Batch("shp-batch-02", "CEILING-FAN", 10, in_two_days)
    late_batch = Batch("shp-batch-03", "CEILING-FAN", 10, in_a_fortnight)
    line = OrderLine("ord-01", "CEILING-FAN", 5)

    allocate(line, [medium_batch, early_batch, late_batch])

    assert late_batch.available_quantity == 10
    assert medium_batch.available_quantity == 10
    assert early_batch.available_quantity == 5


def test_prefers_earliest_batch_with_required_quantity():
    insufficient_stock = Batch("shp-batch-01", "TURBO-BRUSH", 10, tomorrow)
    early = Batch("shp-batch-02", "TURBO-BRUSH", 20, in_two_days)
    late = Batch("shp-batch-03", "TURBO-BRUSH", 60, in_a_fortnight)
    line = OrderLine("ord-01", "TURBO-BRUSH", 15)

    allocate(line, [insufficient_stock, early, late])

    assert late.available_quantity == 60
    assert early.available_quantity == 5
    assert insufficient_stock.available_quantity == 10


def test_raises_out_of_stock_when_cannot_allocate():
    small_batch, large_line = make_batch_and_line("KIWI-CLIPPER", 10, 55)

    with pytest.raises(OutOfStock):
        allocate(large_line, [small_batch])


def test_returns_allocated_batch_reference():
    batch, line = make_batch_and_line("BAMBOO-COUNTERTOP", 100, 5)

    ref = allocate(line, [batch])

    assert ref == batch.ref
