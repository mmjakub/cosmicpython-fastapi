from dataclasses import dataclass
from datetime import date
from typing import Iterable


@dataclass(frozen=True)
class OrderLine:
    order_id: str
    sku: str
    quantity: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: date | None = None):
        self.ref = ref
        self.sku = sku
        self.eta = eta
        self._base_quantity = qty
        self._allocations: set[OrderLine] = set()

    @property
    def available_quantity(self) -> int:
        return self._base_quantity - sum(line.quantity for line in self._allocations)

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.quantity

    def allocate(self, line: OrderLine) -> None:
        if self.can_allocate(line):
            self._allocations.add(line)
        else:
            raise IllegalAllocation

    def deallocate(self, line: OrderLine) -> None:
        self._allocations.discard(line)

    def __lt__(self, other):
        return self.eta is None or other.eta and self.eta < other.eta


def allocate(line: OrderLine, batches: Iterable[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.ref
    except StopIteration:
        raise OutOfStock(f"Not enough stock to allocate {line.quantity} {line.sku}")


class IllegalAllocation(Exception):
    pass


class OutOfStock(Exception):
    pass
