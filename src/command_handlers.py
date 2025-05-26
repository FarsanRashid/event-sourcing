import uuid

from cart import Cart
from commands import AddItem, CreateCart, RemoveItem
from event_store import EventStore


class CommandHandler:
    def __init__(self, event_store: EventStore) -> None:
        self._event_store = event_store

    def _get_stream_name(self, cart_id: uuid.UUID):
        return "cart-" + str(cart_id)

    def _load_aggregate(self, cart_id: uuid.UUID):
        events = self._event_store.get_events(self._get_stream_name(cart_id))
        cart = Cart(events)
        cart.uncommited_events.clear()
        return cart


class CreateCartHandler(CommandHandler):
    def handle(self, command: CreateCart):
        cart = Cart.create(command.customer_id)
        self._event_store.commit_events(
            self._get_stream_name(cart.cart_id), cart.uncommited_events)
        return cart


class AddItemHandler(CommandHandler):
    def handle(self, command: AddItem):
        cart = self._load_aggregate(command.cart_id)
        cart.add_item(command.item)
        self._event_store.commit_events(
            self._get_stream_name(cart.cart_id), cart.uncommited_events)


class RemoveItemHandler(CommandHandler):
    def handle(self, command: RemoveItem):
        cart = self._load_aggregate(command.cart_id)
        cart.remove_item(command.item)
        self._event_store.commit_events(
            self._get_stream_name(cart.cart_id), cart.uncommited_events)
