from sqlalchemy import Column, Integer, String, Table, Date, ForeignKey
from sqlalchemy.orm import registry, relationship

from model import OrderLine, Batch

mapper_registry = registry()

order_line_table = Table(
    "order_line",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", String),
    Column("sku", String),
    Column("quantity", Integer),
)

mapper_registry.map_imperatively(OrderLine, order_line_table)

batch_table = Table(
    "batch",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("ref", String),
    Column("sku", String),
    Column("qty", Integer),
    Column("eta", Date, nullable=True),
)

allocation_table = Table(
    "allocation",
    mapper_registry.metadata,
    Column("order_line_id", ForeignKey(order_line_table.c.id)),
    Column("batch_id", ForeignKey(batch_table.c.id)),
)

mapper_registry.map_imperatively(
    Batch,
    batch_table,
    properties={
        "_base_quantity": batch_table.c.qty,
        "_allocations": relationship(
            OrderLine, secondary=allocation_table, collection_class=set
        ),
    },
)
