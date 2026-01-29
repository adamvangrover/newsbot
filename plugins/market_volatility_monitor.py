import logging
from app.core.event_bus import event_bus

logger = logging.getLogger("MarketVolatilityPlugin")

class Plugin:
    def __init__(self):
        self.description = "Monitors market events for volatility spikes."

    def on_load(self):
        logger.info("MarketVolatilityPlugin loaded.")

    def on_enable(self):
        logger.info("MarketVolatilityPlugin enabled.")
        # Subscribe to events
        # event_bus.subscribe("market_event", self.handle_event)

    def on_disable(self):
        logger.info("MarketVolatilityPlugin disabled.")

    async def handle_event(self, data):
        logger.info(f"Processing event: {data}")
