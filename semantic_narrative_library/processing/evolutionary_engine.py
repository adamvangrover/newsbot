from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
import random
import logging
from pydantic import BaseModel
from .impact_analysis_engine import ImpactAnalyzer, TraceImpact, ImpactAnalysisResult
from synthetic.pydantic_models import NewsArticleMetadata

logger = logging.getLogger(__name__)

class FutureScenario(BaseModel):
    scenario_id: str
    base_date: datetime
    target_date: datetime
    trigger_event: str
    projected_state: str
    likelihood: float
    key_drivers: List[str]
    fitness_score: float = 0.0

# --- RESTORED CLASS ---
class EvolutionarySimulator:
    """
    Simulates how current events might evolve over time (T+1 month, T+6 months)
    using probabilistic mutation of impact chains.
    """
    def __init__(self):
        self.impact_analyzer = ImpactAnalyzer()

    def generate_evolutionary_scenarios(self, initial_event: str, iterations: int = 3) -> List[FutureScenario]:
        scenarios = []
        base_date = datetime.now()

        # 1. Get initial impacts
        dummy_news = NewsArticleMetadata(
            article_id=random.randint(1000, 9999),
            headline=initial_event,
            article_url="http://synthetic",
            publish_timestamp_utc=base_date,
            ingestion_timestamp=base_date,
            source_api="Simulation",
            tickers_mentioned=["SPY", "QQQ"]
        )

        initial_result = self.impact_analyzer.analyze_news(dummy_news)

        if not initial_result.impact_chains:
            scenarios.append(FutureScenario(
                scenario_id=f"sim_default_{int(datetime.now().timestamp())}",
                base_date=base_date,
                target_date=base_date + timedelta(days=30),
                trigger_event=initial_event,
                projected_state="Market absorbs the news with neutral impact.",
                likelihood=0.9,
                key_drivers=["Market Resilience"]
            ))
            return scenarios

        # 2. Evolve
        for i in range(iterations):
            mutation_factor = random.random()
            chain = random.choice(initial_result.impact_chains)
            future_date = base_date + timedelta(days=30 * (i+1))

            if "Drop" in chain.impact_type or "Negative" in chain.impact_type or "Drag" in chain.impact_type:
                outcome = "Recovery Phase" if mutation_factor > 0.6 else "Deepening Correction"
            else:
                outcome = "Growth Continues" if mutation_factor > 0.4 else "Correction due to Overheating"

            scenarios.append(FutureScenario(
                scenario_id=f"sim_{i}_{int(datetime.now().timestamp())}",
                base_date=base_date,
                target_date=future_date,
                trigger_event=initial_event,
                projected_state=f"{outcome} driven by {chain.logic_path}",
                likelihood=round(random.random(), 2),
                key_drivers=[chain.source_entity, chain.target_entity]
            ))

        return scenarios

# --- NEW ADDITIVE CLASS ---
class GeneticEvolutionEngine:
    """
    Implements a Genetic Algorithm to evolve future market scenarios.
    """
    def __init__(self, population_size: int = 10, mutation_rate: float = 0.1):
        self.impact_analyzer = ImpactAnalyzer()
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generation_count = 0
        self.population: List[FutureScenario] = []

    def initialize_population(self, initial_event: str) -> List[FutureScenario]:
        """Creates the initial population based on the seed event."""
        self.population = []
        base_date = datetime.now()

        # Use ImpactAnalyzer to seed the population with realistic logic
        dummy_news = NewsArticleMetadata(
            article_id=random.randint(1000, 9999),
            headline=initial_event,
            article_url="http://synthetic",
            publish_timestamp_utc=base_date,
            ingestion_timestamp=base_date,
            source_api="Simulation",
            tickers_mentioned=["SPY", "QQQ"]
        )
        initial_result = self.impact_analyzer.analyze_news(dummy_news)

        # Create variations for the initial population
        for i in range(self.population_size):
            likelihood = random.uniform(0.1, 0.9)

            # Try to base it on real analysis if possible
            if initial_result.impact_chains and random.random() > 0.3:
                 chain = random.choice(initial_result.impact_chains)
                 state = f"{chain.impact_type} scenario: {chain.description}"
                 drivers = [chain.source_entity, chain.target_entity]
            else:
                 # Fallback/Variation
                 if likelihood > 0.7:
                     state = f"High impact outcome for {initial_event}"
                 elif likelihood > 0.4:
                     state = f"Moderate impact outcome for {initial_event}"
                 else:
                     state = f"Low impact outcome for {initial_event}"
                 drivers = ["Market Volatility", "Sector Rotation"]

            scenario = FutureScenario(
                scenario_id=f"gen0_ind{i}_{int(base_date.timestamp())}",
                base_date=base_date,
                target_date=base_date + timedelta(days=random.randint(30, 180)),
                trigger_event=initial_event,
                projected_state=state,
                likelihood=likelihood,
                key_drivers=drivers
            )
            self.population.append(scenario)

        self.generation_count = 0
        return self.population

    def calculate_fitness(self, scenario: FutureScenario) -> float:
        """
        Determines how 'fit' a scenario is.
        For this simulation, fitness is a function of likelihood and 'impact magnitude' (simulated).
        """
        score = scenario.likelihood * 100
        if "High" in scenario.projected_state or "Surge" in scenario.projected_state:
            score += 20
        elif "Moderate" in scenario.projected_state:
            score += 10

        # Penalize extreme dates
        days_diff = (scenario.target_date - scenario.base_date).days
        if days_diff > 365:
            score -= 10

        return max(0.0, score)

    def selection(self) -> List[FutureScenario]:
        """Selects the best scenarios to be parents for the next generation."""
        # Sort by fitness
        for ind in self.population:
            ind.fitness_score = self.calculate_fitness(ind)

        sorted_pop = sorted(self.population, key=lambda x: x.fitness_score, reverse=True)
        # Elitism: Keep top 20%
        cutoff = int(self.population_size * 0.2)
        return sorted_pop[:max(1, cutoff)]

    def crossover(self, parent1: FutureScenario, parent2: FutureScenario) -> FutureScenario:
        """Combines two parents to create a child."""
        # Child takes likelihood from parent1, outcome text from parent2
        child_state = f"{parent2.projected_state} (influenced by {parent1.key_drivers[0] if parent1.key_drivers else 'unknown'})"

        child = FutureScenario(
            scenario_id=f"gen{self.generation_count+1}_{random.randint(1000,9999)}",
            base_date=parent1.base_date,
            target_date=parent1.target_date, # Inherit date
            trigger_event=parent1.trigger_event,
            projected_state=child_state,
            likelihood=(parent1.likelihood + parent2.likelihood) / 2,
            key_drivers=list(set(parent1.key_drivers + parent2.key_drivers))[:3]
        )
        return child

    def mutate(self, individual: FutureScenario) -> FutureScenario:
        """Randomly alters an individual."""
        if random.random() < self.mutation_rate:
            # Flip likelihood
            individual.likelihood = random.random()
            # Add a random driver
            new_drivers = ["Inflation", "Geopolitics", "Tech Disruption", "Regulation"]
            individual.key_drivers.append(random.choice(new_drivers))
            individual.projected_state += " [MUTATED]"
        return individual

    def run_generation(self) -> List[FutureScenario]:
        """Runs one step of evolution."""
        if not self.population:
            return []

        parents = self.selection()
        next_gen = parents[:] # Keep elites

        while len(next_gen) < self.population_size:
            p1 = random.choice(parents)
            p2 = random.choice(parents)
            child = self.crossover(p1, p2)
            child = self.mutate(child)
            next_gen.append(child)

        self.population = next_gen
        self.generation_count += 1
        logger.info(f"Evolutionary Engine: Generation {self.generation_count} complete.")
        return self.population
