from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import registry

from model import OrderLine

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
