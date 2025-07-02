from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any, Optional

# Adjust relative imports based on how this API will be run.
# If run with `uvicorn semantic_narrative_library.api.main:app --reload` from the repo root,
# these imports should work.
from ..core_models.python.base_types import KnowledgeGraphData, NarrativeEntity, Company, Driver, Relationship, SemanticLink, ConcreteEntityUnion
from ..data.load_sample_data import load_knowledge_graph_from_json
from ..reasoning_engine.simple_reasoner import SimpleReasoner

# --- Globals ---
# In a production app, you might manage these instances differently (e.g., dependency injection)
app = FastAPI(
    title="Semantic Narrative Library API",
    description="API for accessing and reasoning over the knowledge graph.",
    version="0.1.0"
)

# Load data and initialize reasoner at startup
# For simplicity, loading directly here. In a larger app, consider lifespan events or dependency injection.
kg_data_instance: Optional[KnowledgeGraphData] = None
reasoner_instance: Optional[SimpleReasoner] = None

@app.on_event("startup")
async def startup_event():
    global kg_data_instance, reasoner_instance
    print("Loading knowledge graph data...")
    kg_data_instance = load_knowledge_graph_from_json()
    if kg_data_instance:
        reasoner_instance = SimpleReasoner(kg_data_instance)
        print("Knowledge graph loaded and reasoner initialized.")
    else:
        print("Failed to load knowledge graph data. API might not function correctly.")
        # You might want to raise an error here or prevent startup if data is critical

# --- Helper to ensure reasoner is available ---
def get_reasoner() -> SimpleReasoner:
    if not reasoner_instance:
        # This can happen if startup failed or if accessed too early.
        # For robustness, you might re-attempt loading or ensure startup completes.
        raise HTTPException(status_code=503, detail="Reasoner not available. Knowledge graph may not have loaded.")
    return reasoner_instance

# --- API Endpoints ---

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Semantic Narrative Library API"}

@app.get("/entities/{entity_id}", response_model=Optional[ConcreteEntityUnion])
async def get_entity(entity_id: str) -> Optional[NarrativeEntity]:
    """
    Retrieve a specific entity (Company, Industry, MacroIndicator) by its ID.
    """
    reasoner = get_reasoner()
    entity = reasoner.get_entity_by_id(entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail=f"Entity with ID '{entity_id}' not found.")
    return entity

@app.get("/drivers/{driver_id}", response_model=Optional[Driver])
async def get_driver(driver_id: str) -> Optional[Driver]:
    """
    Retrieve a specific driver by its ID.
    """
    reasoner = get_reasoner()
    driver = reasoner.get_driver_by_id(driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail=f"Driver with ID '{driver_id}' not found.")
    return driver

@app.get("/companies/{company_id}/details", response_model=Optional[Company])
async def get_company_details(company_id: str) -> Optional[Company]:
    """
    Retrieve details for a specific company by its ID.
    """
    reasoner = get_reasoner()
    entity = reasoner.get_entity_by_id(company_id)
    if not entity:
        raise HTTPException(status_code=404, detail=f"Company with ID '{company_id}' not found.")
    if not isinstance(entity, Company):
        raise HTTPException(status_code=404, detail=f"Entity with ID '{company_id}' is not a Company (type: {entity.type}).")
    return entity


@app.get("/companies/{company_id}/direct_drivers", response_model=List[Dict[str, Any]])
async def get_company_direct_drivers(company_id: str):
    """
    Get a list of drivers directly impacting the specified company, with explanations.
    """
    reasoner = get_reasoner()
    # First, check if the company exists and is indeed a company
    company_entity = reasoner.get_entity_by_id(company_id)
    if not company_entity:
        raise HTTPException(status_code=404, detail=f"Company with ID '{company_id}' not found.")
    if not isinstance(company_entity, Company): # or company_entity.type != "Company"
        raise HTTPException(status_code=400, detail=f"Entity '{company_id}' is not a Company.")

    drivers_info = reasoner.find_direct_drivers_for_company(company_id)
    if not drivers_info and not company_entity: #This check is redundant due to above
        pass # find_direct_drivers_for_company handles non-existent company internally, but good to be sure
    return drivers_info

@app.get("/companies/{company_id}/narrative", response_model=str)
async def get_company_narrative(company_id: str):
    """
    Generate a simple narrative about the key drivers for the specified company.
    """
    reasoner = get_reasoner()
    # Check if company exists
    company_entity = reasoner.get_entity_by_id(company_id)
    if not company_entity:
        raise HTTPException(status_code=404, detail=f"Company with ID '{company_id}' not found.")
    if not isinstance(company_entity, Company):
         raise HTTPException(status_code=400, detail=f"Entity '{company_id}' is not a Company.")

    narrative = reasoner.generate_simple_narrative_for_company_drivers(company_id)
    return narrative

@app.get("/knowledge_graph/stats")
async def get_kg_stats():
    """
    Get basic statistics about the loaded knowledge graph.
    """
    reasoner = get_reasoner()
    if not reasoner.kg_data:
         raise HTTPException(status_code=503, detail="Knowledge graph data not loaded.")
    return {
        "num_entities": len(reasoner.kg_data.entities),
        "num_drivers": len(reasoner.kg_data.drivers),
        "num_relationships": len(reasoner.kg_data.relationships),
        "num_semantic_links": len(reasoner.kg_data.semantic_links) if reasoner.kg_data.semantic_links else 0,
    }

# To run this app:
# 1. Ensure your terminal is in the root directory of the repository.
# 2. Run: uvicorn semantic_narrative_library.api.main:app --reload
# Then access via browser or API client at http://127.0.0.1:8000
# API docs will be at http://127.0.0.1:8000/docs
# OpenAPI spec at http://127.0.0.1:8000/openapi.json

# --- Placeholder Endpoints for Advanced Framework ---

# @app.post("/analyze/news_item_impact", status_code=501) # 501 Not Implemented
# async def analyze_news_item_impact(news_item_id: str, target_company_id: str):
#     """
#     (Future Endpoint) Analyzes a news item, identifies its significance,
#     traces its potential impact on a specified company, and generates a narrative.
#     This would trigger a workflow involving NLProcessor, SignificanceScorer, ImpactAnalyzer.
#     """
#     # Conceptual:
#     # 1. Fetch NewsItem and Company entities.
#     # 2. Use NLProcessor if news_item needs enhancement.
#     # 3. Use SignificanceScorer.
#     # 4. Use ImpactAnalyzer.
#     # 5. Use (Simulated)NarrativeGenerator for detailed output.
#     return {"message": "Endpoint not yet implemented."}

# @app.post("/scenarios/run_what_if", status_code=501)
# async def run_what_if_scenario(scenario_definition: Dict[str, Any]):
#     """
#     (Future Endpoint) Runs a 'what-if' scenario based on a provided definition.
#     This would use the ScenarioModeler and other processing components.
#     """
#     # Conceptual:
#     # 1. Get base_knowledge_graph from reasoner_instance.kg_data.
#     # 2. Instantiate ScenarioModeler.
#     # 3. Call scenario_modeler.run_what_if_scenario(base_kg, scenario_definition).
#     return {"message": "Endpoint not yet implemented.", "received_scenario": scenario_definition}

# @app.post("/ingest/news_feed", status_code=501)
# async def ingest_news_feed_source(feed_url: str, source_name: str):
#     """
#     (Future Endpoint) Ingests news from a given feed URL.
#     This would use the DataIngestor and potentially update the knowledge graph.
#     (Requires KG to be mutable and have persistence).
#     """
#     # Conceptual:
#     # 1. Instantiate DataIngestor.
#     # 2. Call data_ingestor.ingest_news_feed(feed_url, source_name).
#     # 3. Process/store the returned NewsItem objects.
#     return {"message": "Endpoint not yet implemented.", "feed_url": feed_url, "source_name": source_name}

if __name__ == "__main__":
    # This block is for direct execution (though uvicorn is preferred for FastAPI)
    # Uvicorn is needed to run the ASGI app.
    # Example: python -m semantic_narrative_library.api.main
    # This won't work directly as main.py is an ASGI app, not a script to run like this.
    # You need an ASGI server like Uvicorn.
    print("To run this FastAPI application, use Uvicorn:")
    print("Example: uvicorn semantic_narrative_library.api.main:app --reload --port 8000")
    print("Ensure you are in the repository's root directory.")
