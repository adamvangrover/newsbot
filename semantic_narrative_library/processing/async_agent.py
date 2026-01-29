import asyncio
import abc
from typing import Dict, Any, List
import logging
from app.core.event_bus import event_bus
from app.core.async_utils import task_manager

logger = logging.getLogger(__name__)

class AsyncAgent(abc.ABC):
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.is_running = False
        self.task_id = None

    async def start(self):
        self.is_running = True
        self.task_id = await task_manager.start_task(f"agent_{self.name}", self._run_loop())
        await event_bus.publish("agent_started", {"name": self.name, "role": self.role})
        logger.info(f"Agent {self.name} started.")

    async def stop(self):
        self.is_running = False
        await event_bus.publish("agent_stopped", {"name": self.name})
        logger.info(f"Agent {self.name} stopping...")

    async def _run_loop(self):
        logger.info(f"[{self.name}] Agent loop initialized.")
        while self.is_running:
            try:
                await self.process()
                await asyncio.sleep(self.get_interval())
            except Exception as e:
                logger.error(f"[{self.name}] Error in loop: {e}")
                await asyncio.sleep(5) # Backoff

    @abc.abstractmethod
    async def process(self):
        pass

    def get_interval(self) -> float:
        return 5.0

class SentimentAgent(AsyncAgent):
    async def process(self):
        # Simulate checking for news and analyzing sentiment
        await asyncio.sleep(0.1)
        # Randomly publish an insight
        import random
        if random.random() < 0.2:
            await event_bus.publish("market_insight", {
                "source": self.name,
                "type": "Sentiment",
                "content": "Bullish sentiment detected in Tech sector.",
                "timestamp": asyncio.get_event_loop().time()
            })

class RiskAgent(AsyncAgent):
    async def process(self):
        await asyncio.sleep(0.1)
        import random
        if random.random() < 0.1:
             await event_bus.publish("risk_alert", {
                "source": self.name,
                "type": "Volatility",
                "content": "Volatility spike detected in Asian markets.",
                "timestamp": asyncio.get_event_loop().time()
            })
