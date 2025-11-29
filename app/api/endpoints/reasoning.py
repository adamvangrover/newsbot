from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from semantic_narrative_library.processing.scenario_engine import reasoning_core
from semantic_narrative_library.processing.impact_analysis_engine import ImpactAnalysisResult
from synthetic.pydantic_models import NewsArticleMetadata

router = APIRouter()

class ScenarioRequest(BaseModel):
    name: str
    events: List[Dict[str, Any]] # Simplified input for flexibility

@router.post("/impact", response_model=ImpactAnalysisResult)
def analyze_impact(news_item: NewsArticleMetadata):
    """
    Analyze the potential impact of a single news article.
    """
    try:
        result = reasoning_core.analyze_impact(news_item)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/simulate", response_model=Dict[str, Any])
def simulate_scenario(request: ScenarioRequest):
    """
    Simulate a scenario based on a list of hypothetical events.
    """
    try:
        # Convert dicts to Pydantic models
        events = []
        for i, event_data in enumerate(request.events):
            # Fill defaults if missing
            if "article_id" not in event_data: event_data["article_id"] = i
            if "publish_timestamp_utc" not in event_data: event_data["publish_timestamp_utc"] = datetime.now()
            if "ingestion_timestamp" not in event_data: event_data["ingestion_timestamp"] = datetime.now()

            events.append(NewsArticleMetadata(**event_data))

        result = reasoning_core.simulate_scenario(request.name, events)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
