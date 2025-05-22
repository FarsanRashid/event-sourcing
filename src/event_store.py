from typing import Dict, List
import uuid

from events import Event


class EventStore:
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
