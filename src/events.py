from dataclasses import asdict, dataclass
import uuid


@dataclass
class Event:
    def to_dict(self):
        data = asdict(self)
        return data


@dataclass
class CartCreated(Event):
    customer_id: str
    cart_id: uuid.UUID

    def to_dict(self):
        data = asdict(self)
        data["cart_id"] = str(self.cart_id)
        return data


@dataclass
class ItemAdded(Event):
    item: str


@dataclass
class ItemRemoved(Event):
    item: str
