from dataclasses import dataclass
import uuid


class Event:
    pass


@dataclass
class CartCreated(Event):
    customer_id: str
    cart_id: uuid.UUID


@dataclass
class ItemAdded(Event):
    item: str


@dataclass
class ItemRemoved(Event):
    item: str
