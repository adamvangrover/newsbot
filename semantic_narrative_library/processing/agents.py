import asyncio
import logging
import random
from datetime import datetime
from .async_agent import AsyncAgent
from .evolutionary_engine import GeneticEvolutionEngine
from app.core.event_bus import event_bus

logger = logging.getLogger(__name__)

class AnalystAgent(AsyncAgent):
    def __init__(self, name: str, sector: str):
        super().__init__(name, f"Analyst ({sector})")
        self.sector = sector

    async def process(self):
        # Check memory for relevant insights
        recent_insights = self.memory.retrieve(self.sector, limit=1)
        if recent_insights:
             # Formulate a plan
             plan = self.planner.plan_action(f"analyze {self.sector}", {"timestamp": datetime.now()})
             logger.info(f"[{self.name}] Executing plan: {plan['actions']}")

             # Simulate analysis
             await asyncio.sleep(0.5)
             await event_bus.publish("sector_analysis", {
                 "sector": self.sector,
                 "analyst": self.name,
                 "verdict": "Outperform" if random.random() > 0.5 else "Underperform"
             })

class CoordinatorAgent(AsyncAgent):
    def __init__(self, name: str):
        super().__init__(name, "Coordinator")

    async def process(self):
        # Simulate orchestration
        if random.random() < 0.05:
            await event_bus.publish("task_dispatch", {
                "source": self.name,
                "task": "Rebalance Portfolio",
                "priority": "High"
            })

class EvolutionaryAgent(AsyncAgent):
    def __init__(self, name: str):
        super().__init__(name, "Evolutionary Simulation")
        self.engine = GeneticEvolutionEngine()
        self.current_population = []

    async def process(self):
        # Run evolution step periodically
        if not self.current_population:
            logger.info(f"[{self.name}] Initializing population...")
            self.current_population = self.engine.initialize_population("Market Crash")
        else:
            self.current_population = self.engine.run_generation()
            best_candidate = self.current_population[0] # Sorted by fitness

            await event_bus.publish("evolution_update", {
                "generation": self.engine.generation_count,
                "best_scenario": best_candidate.projected_state,
                "fitness": best_candidate.fitness_score
            })

        await asyncio.sleep(2) # Run slower than others
