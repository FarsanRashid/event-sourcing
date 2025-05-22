from typing import List
import uuid

from events import CartCreated, Event, ItemAdded, ItemRemoved


class Cart:
    def __init__(self, events: List[Event]) -> None:
        self.cart_id: uuid.UUID
        self.customer_id: str
        self.uncommited_events: List[Event] = []
        self._version: int = 0
        self._items: List[str] = []

        for event in events:
            self._apply(event)

    def __repr__(self) -> str:
        return f"Cart(cart_id={self.cart_id}, customer_id={self.customer_id}, items={self._items}, self.version={self._version})"

    def _apply(self, event: Event):
        if isinstance(event, CartCreated):
            self.cart_id = event.cart_id
            self.customer_id = event.customer_id
        elif isinstance(event, ItemAdded):
            self._items.append(event.item)
        elif isinstance(event, ItemRemoved):
            self._items.remove(event.item)

        self._version = self._version + 1
        self.uncommited_events.append(event)

    @classmethod
    def create(cls, customer_id: str):
        cart_id = uuid.uuid4()
        event = CartCreated(customer_id, cart_id)
        cart = Cart([event])
        return cart

    def add_item(self, item: str):
        event = ItemAdded(item)
        self._apply(event)

    def remove_item(self, item: str):
        event = ItemRemoved(item)
        self._apply(event)
