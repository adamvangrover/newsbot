from typing import List, Optional, Dict, Any, Union, Tuple, Literal, Annotated
from pydantic import BaseModel, Field, ConfigDict, RootModel
from datetime import datetime

class NarrativeEntity(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: str
    name: str
    description: Optional[str] = None
    type: str  # e.g., "Industry", "Company", "MacroIndicator"
    attributes: Optional[Dict[str, Any]] = Field(default_factory=dict)
    tags: Optional[List[str]] = Field(default_factory=list)

class Driver(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: str
    name: str
    description: str
    impact_potential: Optional[Union[str, float]] = None # 'High', 'Medium', 'Low', or a numeric score
    influence_pattern: Optional[str] = None # How this driver typically influences things
    related_entity_types: Optional[List[str]] = Field(default_factory=list)
    tags: Optional[List[str]] = Field(default_factory=list)

class Relationship(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: str
    source_id: str  # ID of the source NarrativeEntity or Driver
    target_id: str  # ID of the target NarrativeEntity or Driver
    type: str  # e.g., "influences", "owns", "competes_with", "is_part_of", "has_driver"
    strength: Optional[float] = None  # e.g., 0.0 to 1.0
    direction: Optional[str] = None # 'unidirectional', 'bidirectional'
    explanation_template: Optional[str] = None  # e.g., "{source_name} {type} {target_name}"
    attributes: Optional[Dict[str, Any]] = Field(default_factory=dict)
    tags: Optional[List[str]] = Field(default_factory=list)

class SemanticLink(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: str
    # ID of the element being linked (e.g., a specific Driver instance affecting a Company, or a generated narrative)
    narrative_element_id: str
    metric_observed: str  # e.g., "StockPrice", "AnalystRating", "SentimentScore"
    # Could be a specific value, a range, or a qualitative observation
    observed_value: Optional[Union[str, float, Tuple[float, float]]] = None
    observation_time: Optional[datetime] = None
    source_of_observation: Optional[str] = None  # Where this link was derived from
    confidence: Optional[float] = None  # e.g., 0.0 to 1.0
    explanation: str  # Why this link/observation is relevant
    tags: Optional[List[str]] = Field(default_factory=list)

# Example of a more specific entity type
class Company(NarrativeEntity):
    type: Literal["Company"] = "Company"
    ticker_symbol: Optional[str] = None
    industry_id: Optional[str] = None
    country: Optional[str] = None

class Industry(NarrativeEntity):
    type: Literal["Industry"] = "Industry"
    sector: Optional[str] = None

class MacroIndicator(NarrativeEntity):
    type: Literal["MacroIndicator"] = "MacroIndicator" # type: ignore # Override NarrativeEntity.type
    region: Optional[str] = Field(default=None, description="Geographical region for the indicator")
    # Add other specific fields for MacroIndicator if needed

class NewsItem(NarrativeEntity):
    type: Literal["NewsItem"] = "NewsItem" # type: ignore
    source_name: Optional[str] = Field(default=None, description="e.g., Reuters, Bloomberg")
    url: Optional[str] = Field(default=None)
    publication_date: Optional[datetime] = None
    sentiment_score: Optional[float] = Field(default=None, ge=-1, le=1)
    key_entities_mentioned_ids: List[str] = Field(default_factory=list, description="List of IDs of other NarrativeEntities mentioned")
    summary: Optional[str] = None # Could be LLM generated or from source

class PoliticalEvent(NarrativeEntity):
    type: Literal["PoliticalEvent"] = "PoliticalEvent" # type: ignore
    location: Optional[str] = None
    event_date: Optional[datetime] = None
    event_subtype: Optional[str] = Field(default=None, description="e.g., Election, Protest, TradeDealAnnouncement")
    involved_parties: List[str] = Field(default_factory=list, description="Names or IDs of involved groups/countries/people")
    perceived_impact_area: Optional[str] = Field(default=None, description="e.g., Geopolitics, SpecificIndustry, HumanRights")

class FinancialReportItem(NarrativeEntity):
    type: Literal["FinancialReportItem"] = "FinancialReportItem" # type: ignore
    company_id: str # Link to the company this report is for
    report_type: Literal["10-K", "10-Q", "8-K", "Annual Report", "Quarterly Report", "Other"]
    period_ending_date: Optional[datetime] = None
    filing_date: Optional[datetime] = None
    key_metrics: Dict[str, Any] = Field(default_factory=dict, description="e.g., {'Revenue': 100M, 'NetIncome': 10M}")
    link_to_report: Optional[str] = None

class MarketSignal(NarrativeEntity):
    type: Literal["MarketSignal"] = "MarketSignal" # type: ignore
    signal_type: str # e.g., "PriceSpike", "VolumeSurge", "AnalystUpgrade", "AnalystDowngrade"
    asset_class: Optional[str] = Field(default=None, description="e.g., Equity, FixedIncome, Commodity, FX")
    security_id: Optional[str] = Field(default=None, description="Link to a specific Security entity if applicable")
    timestamp: datetime
    details: Dict[str, Any] = Field(default_factory=dict, description="e.g., {'old_price': 100, 'new_price': 110}")

class RegulatoryChange(NarrativeEntity):
    type: Literal["RegulatoryChange"] = "RegulatoryChange" # type: ignore
    jurisdiction: str
    agency: Optional[str] = None
    status: Literal["Proposed", "Enacted", "Repealed", "Guidance"]
    summary: str
    effective_date: Optional[datetime] = None
    industries_affected_ids: List[str] = Field(default_factory=list)

class Security(NarrativeEntity): # Name can be Ticker or CUSIP for example
    type: Literal["Security"] = "Security" # type: ignore
    issuer_id: Optional[str] = Field(default=None, description="ID of the issuing Company or entity")
    security_subtype: str # E.g., "CommonStock", "PreferredStock", "CorporateBond", "GovernmentBond"
    ticker: Optional[str] = None # Stock ticker
    cusip: Optional[str] = None
    isin: Optional[str] = None
    exchange: Optional[str] = Field(default=None, description="e.g., NYSE, NASDAQ")


# Define a discriminated union for entity types including new ones
ConcreteEntityUnion = Annotated[
    Union[
        Company,
        Industry,
        MacroIndicator,
        NewsItem,
        PoliticalEvent,
        FinancialReportItem,
        MarketSignal,
        RegulatoryChange,
        Security
        # Add future concrete entity types here
    ],
    Field(discriminator='type')
]


# This will be the core of our knowledge graph, likely a collection of entities and relationships
class KnowledgeGraphData(BaseModel):
    # Now, Pydantic will use the 'type' field to determine which model to use for each item in entities
    entities: List[ConcreteEntityUnion] = Field(default_factory=list)
    drivers: List[Driver] = Field(default_factory=list)
    relationships: List[Relationship] = Field(default_factory=list)
    semantic_links: Optional[List[SemanticLink]] = Field(default_factory=list)

# Example usage (optional, for testing)
if __name__ == "__main__":
    # Now, Pydantic will use the 'type' field to determine which model to use for each item in entities
    entities: List[EntityUnion] = Field(default_factory=list)
    drivers: List[Driver] = Field(default_factory=list)
    relationships: List[Relationship] = Field(default_factory=list)
    semantic_links: Optional[List[SemanticLink]] = Field(default_factory=list)

# Example usage (optional, for testing)
if __name__ == "__main__":
    sample_company = Company(id="comp_001", name="TechCorp", ticker_symbol="TCRP", industry_id="ind_tech", country="USA")
    sample_industry = Industry(id="ind_tech", name="Technology", sector="Information Technology")
    sample_driver = Driver(id="drv_001", name="AI Adoption", description="Increased adoption of AI technologies.", impact_potential="High")
    sample_relationship = Relationship(
        id="rel_001",
        source_id="drv_001",
        target_id="comp_001",
        type="positively_influences",
        strength=0.8,
        explanation_template="{source_name} is {type} {target_name}'s growth prospects."
    )
    sample_link = SemanticLink(
        id="slink_001",
        narrative_element_id="rel_001",
        metric_observed="StockPriceOutlook",
        observed_value="Positive",
        explanation="Strong AI adoption is expected to boost TechCorp's future earnings."
    )

    kg_data = KnowledgeGraphData(
        entities=[sample_company, sample_industry],
        drivers=[sample_driver],
        relationships=[sample_relationship],
        semantic_links=[sample_link]
    )

    print(kg_data.json(indent=2))
