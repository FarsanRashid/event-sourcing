from abc import ABC, abstractmethod
import json
from typing import Dict, List
import uuid

from kurrentdbclient import KurrentDBClient, NewEvent, StreamState
from kurrentdbclient import RecordedEvent

from events import CartCreated, Event, ItemAdded, ItemRemoved


class EventStore(ABC):
    @abstractmethod
    def commit_events(self, id: uuid.UUID, events: List[Event]):
        raise NotImplementedError

    @abstractmethod
    def get_events(self, id: uuid.UUID):
        raise NotImplementedError


class InMemoryEventStore(EventStore):
    def __init__(self) -> None:
        self._event_store: Dict[uuid.UUID, List[Event]] = {}

    def commit_events(self, id: uuid.UUID, events: List[Event]):
        for event in events:
            if id in self._event_store:
                self._event_store[id].append(event)
            else:
                self._event_store[id] = [event]

    def get_events(self, id: uuid.UUID):
        return self._event_store[id]


class EventStoreDB(EventStore):
    def __init__(self) -> None:
        self.EVENT_TYPE_MAP = {
            "CartCreated": CartCreated,
            "ItemAdded": ItemAdded,
            "ItemRemoved": ItemRemoved,
        }
        self._event_store = KurrentDBClient(
            uri="esdb://localhost:2113?tls=false")

    def commit_events(self, id: uuid.UUID, events: List[Event]):
        for event in events:
            new_event = NewEvent(
                type=event.__class__.__name__,
                data=json.dumps(event.to_dict()).encode("utf-8"),
                content_type="application/json",
            )
            self._event_store.append_to_stream(
                stream_name=str(id),
                events=[new_event],
                current_version=StreamState.ANY,
            )

    def get_event_type(self, event_type: RecordedEvent):
        cls = self.EVENT_TYPE_MAP[event_type.type]
        return cls(**json.loads(event_type.data.decode("utf-8")))

    def get_events(self, id: uuid.UUID):
        events = self._event_store.get_stream(
            stream_name=str(id),
            stream_position=0,
            limit=100,
        )
        return [self.get_event_type(event) for event in events]
