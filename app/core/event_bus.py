import asyncio
from typing import Callable, List, Dict, Any, Awaitable
import logging

logger = logging.getLogger(__name__)

class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable[[Dict[str, Any]], Awaitable[None]]]] = {}

    def subscribe(self, event_type: str, handler: Callable[[Dict[str, Any]], Awaitable[None]]):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
        logger.info(f"Subscribed to {event_type}")

    async def publish(self, event_type: str, data: Dict[str, Any]):
        # Notify system monitor implicitly if we had circular imports, but better to keep it clean.
        # We can add a 'system' channel later.
        if event_type in self.subscribers:
            for handler in self.subscribers[event_type]:
                try:
                    asyncio.create_task(handler(data))
                except Exception as e:
                    logger.error(f"Error handling event {event_type}: {e}")

# Global instance
event_bus = EventBus()
