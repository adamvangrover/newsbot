import asyncio
from typing import List, Dict, Any
from semantic_narrative_library.processing.async_agent import SentimentAgent, RiskAgent
from semantic_narrative_library.processing.agents import AnalystAgent, CoordinatorAgent, EvolutionaryAgent

class CognitiveService:
    def __init__(self):
        self.agents = []
        self._initialize_agents()

    def _initialize_agents(self):
        self.agents.append(SentimentAgent("SentimentBot", "Sentiment"))
        self.agents.append(RiskAgent("RiskBot", "Risk"))
        self.agents.append(AnalystAgent("TechAnalyst", "Technology"))
        self.agents.append(CoordinatorAgent("MasterMind"))
        self.agents.append(EvolutionaryAgent("EvoSim"))

    async def start_all(self):
        for agent in self.agents:
            if not agent.is_running:
                await agent.start()

    async def stop_all(self):
        for agent in self.agents:
            if agent.is_running:
                await agent.stop()

    def get_agent_status(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": agent.name,
                "role": agent.role,
                "status": "Running" if agent.is_running else "Stopped",
                "memory_size": len(agent.memory.get_all())
            }
            for agent in self.agents
        ]

    def get_evolution_status(self) -> Dict[str, Any]:
        evo_agent = next((a for a in self.agents if isinstance(a, EvolutionaryAgent)), None)
        if evo_agent and evo_agent.current_population:
             best = evo_agent.current_population[0]
             return {
                 "generation": evo_agent.engine.generation_count,
                 "best_scenario": best.projected_state,
                 "fitness": best.fitness_score
             }
        return {"status": "Not initialized"}

cognitive_service = CognitiveService()
