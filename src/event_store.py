from abc import ABC, abstractmethod
import json
from typing import Dict, List

from kurrentdbclient import KurrentDBClient, NewEvent, StreamState
from kurrentdbclient import RecordedEvent

from events import CartCreated, Event, ItemAdded, ItemRemoved


class EventStore(ABC):
    @abstractmethod
    def commit_events(self, stream_name: str, events: List[Event]):
        raise NotImplementedError

    @abstractmethod
    def get_events(self, stream_name: str):
        raise NotImplementedError


class InMemoryEventStore(EventStore):
    def __init__(self) -> None:
        self._event_store: Dict[str, List[Event]] = {}

    def commit_events(self, stream_name: str, events: List[Event]):
        for event in events:
            if stream_name in self._event_store:
                self._event_store[stream_name].append(event)
            else:
                self._event_store[stream_name] = [event]

    def get_events(self, stream_name: str):
        return self._event_store[stream_name]


class EventStoreDB(EventStore):
    def __init__(self) -> None:
        self.EVENT_TYPE_MAP = {
            "CartCreated": CartCreated,
            "ItemAdded": ItemAdded,
            "ItemRemoved": ItemRemoved,
        }
        self._event_store = KurrentDBClient(
            uri="esdb://localhost:2113?tls=false")

    def commit_events(self, stream_name: str, events: List[Event]):
        for event in events:
            new_event = NewEvent(
                type=event.__class__.__name__,
                data=json.dumps(event.to_dict()).encode("utf-8"),
                content_type="application/json",
            )
            self._event_store.append_to_stream(
                stream_name=stream_name,
                events=[new_event],
                current_version=StreamState.ANY,
            )

    def get_event_type(self, event_type: RecordedEvent):
        cls = self.EVENT_TYPE_MAP[event_type.type]
        return cls(**json.loads(event_type.data.decode("utf-8")))

    def get_events(self, stream_name: str):
        events = self._event_store.get_stream(
            stream_name=stream_name,
            stream_position=0,
            limit=100,
        )
        return [self.get_event_type(event) for event in events]
