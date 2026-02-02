import pytest
from semantic_narrative_library.cognitive.memory import MemoryStore
from semantic_narrative_library.cognitive.planner import CognitivePlanner
from semantic_narrative_library.processing.evolutionary_engine import GeneticEvolutionEngine, FutureScenario, EvolutionarySimulator

def test_memory_store():
    store = MemoryStore(capacity=2)
    store.add("Event 1", {"tag": "A"})
    store.add("Event 2", {"tag": "B"})
    store.add("Event 3", {"tag": "C"})

    assert len(store.get_all()) == 2
    assert store.get_all()[1]["content"] == "Event 3"

    results = store.retrieve("Event 3")
    assert len(results) == 1
    assert results[0]["metadata"]["tag"] == "C"

def test_planner():
    planner = CognitivePlanner()
    plan = planner.plan_action("analyze market", {})
    assert "fetch_data" in plan["actions"]
    assert plan["strategy"] == "heuristic"

def test_evolution_engine():
    engine = GeneticEvolutionEngine(population_size=4)
    pop = engine.initialize_population("Trigger")
    assert len(pop) == 4

    # Run one generation
    next_gen = engine.run_generation()
    assert len(next_gen) == 4
    assert engine.generation_count == 1

def test_evolution_simulator_legacy():
    sim = EvolutionarySimulator()
    scenarios = sim.generate_evolutionary_scenarios("Legacy Event", iterations=2)
    assert len(scenarios) >= 1
    assert scenarios[0].trigger_event == "Legacy Event"
