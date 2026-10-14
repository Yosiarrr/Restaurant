from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Customer:
    id: int | None = None
    name: str = ""
    phone: str = ""
    email: str = ""


@dataclass
class RestaurantTable:
    id: int | None = None
    table_number: int = 0
    capacity: int = 0
    status: str = "available"


@dataclass
class OrderItem:
    id: int | None = None
    order_id: int | None = None
    menu_name: str = ""
    quantity: int = 1
    unit_price: float = 0.0

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class Order:
    id: int | None = None
    customer_id: int | None = None
    table_id: int | None = None
    created_at: str | None = None
    total_amount: float = 0.0
    status: str = "open"
    items: list[OrderItem] = field(default_factory=list)

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
