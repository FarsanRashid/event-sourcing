from cart import Cart
from command_handlers import CreateCartHandler, RemoveItemHandler
from command_handlers import AddItemHandler
from commands import CreateCart, RemoveItem
from commands import AddItem
from event_store import EventStoreDB, InMemoryEventStore

event_store = EventStoreDB()

# event_store = InMemoryEventStore()

# create a cart
handler = CreateCartHandler(event_store)
cart = handler.handle(CreateCart("farsan"))

# add items to cart
handler = AddItemHandler(event_store)
handler.handle(AddItem(cart.cart_id, "apple"))
handler.handle(AddItem(cart.cart_id, "banana"))
handler.handle(AddItem(cart.cart_id, "banana"))
handler.handle(AddItem(cart.cart_id, "orange"))

# remove a item
handler = RemoveItemHandler(event_store)
handler.handle(RemoveItem(cart.cart_id, "apple"))

events = event_store.get_events(cart.cart_id)
cart = Cart(events)
print(events)
print(cart)
