import pytest

from model import Batch, OrderLine, IllegalAllocation


def make_batch_and_line(sku: str, batch_quantity: int, line_quantity: int) -> tuple[Batch, OrderLine]:
    batch = Batch("test-batch-1", sku, batch_quantity, None)
    line = OrderLine("test-order-1", sku, line_quantity)
    return batch, line


def test_cannot_allocate_if_line_sku_does_not_match_batch():
    batch = Batch("test-batch-1", "QT-OCTOPUS-PLUSH", 8, None)
    different_sku_line = OrderLine("test-order-1", "PIRATE-STATUETTE", 7)

    assert not batch.can_allocate(different_sku_line)


def test_allocate_raises_error_if_sku_does_not_match_batch():
    batch = Batch("test-batch-1", "QT-OCTOPUS-PLUSH", 8, None)
    different_sku_line = OrderLine("test-order-1", "PIRATE-STATUETTE", 7)

    with pytest.raises(IllegalAllocation):
        batch.allocate(different_sku_line)


def test_can_allocate_if_enough_items_are_available_in_batch():
    sufficient_batch, line = make_batch_and_line("TUNING-FORK", 10, 5)

    assert sufficient_batch.can_allocate(line)


def test_cannot_allocate_if_line_quantity_exceeds_available_stock():
    insufficient_batch, line = make_batch_and_line("COFFEE-TABLE", 3, 7)

    assert not insufficient_batch.can_allocate(line)


def test_allocate_raises_error_if_quantity_exceeds_available_stock():
    insufficient_batch, line = make_batch_and_line("COFFEE-TABLE", 3, 7)

    with pytest.raises(IllegalAllocation):
        insufficient_batch.allocate(line)


def test_available_quantity_decreases_after_allocating_a_line():
    batch, line = make_batch_and_line("STOLEN-CHEESE", 4, 2)

    batch.allocate(line)

    assert batch.available_quantity == 2


def test_allocation_is_idempotent():
    batch, line = make_batch_and_line("GIANT-JALAPENO-CUSHIONS", 120, 42)

    batch.allocate(line)
    batch.allocate(line)

    assert batch.available_quantity == 78


def test_quantity_is_restored_after_deallocating_a_line():
    batch, line = make_batch_and_line("VICTORIAN-HAT-RACK", 30, 5)
    batch.allocate(line)

    batch.deallocate(line)

    assert batch.available_quantity == 30


def test_only_allocated_lines_are_deallocated():
    batch, line = make_batch_and_line("GARDEN-CHAIR-SET", 10, 2)

    batch.deallocate(line)

    assert batch.available_quantity == 10
