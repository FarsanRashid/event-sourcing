from dataclasses import dataclass
import uuid


@dataclass
class CreateCart:
    customer_id: str


@dataclass
class AddItem:
    cart_id: uuid.UUID
    item: str


@dataclass
class RemoveItem:
    cart_id: uuid.UUID
    item: str
