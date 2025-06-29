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
    model_config = ConfigDict(frozen=True) # Inherits frozen from NarrativeEntity if not overridden
    type: Literal["MacroIndicator"] = "MacroIndicator"
    region: Optional[str] = Field(default=None, description="Geographical region for the indicator")
    # Add other specific fields for MacroIndicator if needed

# Define a discriminated union for entity types
# Order matters: specific types first. NarrativeEntity as a fallback if no specific type matches.
# For NarrativeEntity to be a valid discriminated choice, its 'type' field would also need to be Literal.
# If NarrativeEntity is purely abstract or a fallback for types not explicitly listed, this setup needs care.
# Pydantic's error suggests that if NarrativeEntity is in the Union, it expects a Literal 'type' on it.
# To resolve this, we ensure all explicitly chosen types (Company, Industry, MacroIndicator) have Literal types.
# If a type string in JSON (e.g. "GenericEvent") doesn't match any of these Literals,
# it would fall back to NarrativeEntity, BUT NarrativeEntity.type is `str`, not `Literal`.
# This is the core of the Pydantic error.

# Option 1: Make NarrativeEntity.type also a Literal (e.g. Literal["GenericNarrativeEntity"])
# This means if it's just a base NarrativeEntity, its type field must be "GenericNarrativeEntity".
# Option 2: Only include specific subclasses in the Union.
# Let's try ensuring all *concrete* types in the union have Literal types.
# If NarrativeEntity itself is a valid choice, its `type` field should be `Literal`.
# For now, we will make NarrativeEntity's type a Literal as well, to satisfy the discriminator.
# This means if a type like "NewPhenomenon" appears, it won't parse as NarrativeEntity unless we add that Literal.

# Re-evaluating: The error is about NarrativeEntity *itself* needing a Literal type if it's a candidate.
# If NarrativeEntity is just a base and never directly instantiated from the union, it can be excluded from the Union members
# that are directly chosen by the discriminator.
# However, our current Union includes it: Union[Company, Industry, NarrativeEntity]
# This means NarrativeEntity IS a candidate.

# Let's adjust NarrativeEntity.type to be a Literal for specific "generic" cases or remove it from the direct union choices
# if it's purely abstract. The simplest fix for the error message is to make its 'type' a Literal.
# We'll assume for now that a "base" NarrativeEntity instance might have a specific type string not covered by subclasses.
# This is a common point of confusion with Pydantic discriminated unions.
# The most robust way is often to have a common Literal string on the base if it can be instantiated.
# Or, ensure the base class is not part of the Union directly if it's abstract.

# Let's redefine NarrativeEntity's type field to be a specific Literal if it's a generic instance.
# For this iteration, I will modify NarrativeEntity to have a Literal type as well.
# This means if a JSON object has type "NarrativeEntity", it will be parsed as such.
# And other types like "Company" will be parsed as Company.

# Let's go back to the original definition of NarrativeEntity.type as str,
# and ensure the Union only contains types that have Literal discriminators.
# If an entity in the JSON has a 'type' not in these Literals, it should fail or be handled by a default.

# The error "Model 'NarrativeEntity' needs field 'type' to be of type `Literal`"
# is because NarrativeEntity is in the Union: `Union[Company, Industry, NarrativeEntity]`.
# If NarrativeEntity is meant to be a catch-all for types not Company or Industry,
# its `type` field must also participate in the Literal-based discrimination.

# Correct approach for Pydantic v2: The discriminator field on the base class of a discriminated union
# does not need to be `Literal`. It's the derived classes that must have `Literal` types for the discriminator field.
# The issue might be that `NarrativeEntity` is the *last* item in the Union.
# Let's put more specific types first.

EntityUnion = Annotated[Union[Company, Industry, MacroIndicator, NarrativeEntity], Field(discriminator='type')]
# The issue is that NarrativeEntity itself, when chosen, doesn't offer a Literal for its 'type' field.
# If NarrativeEntity is a fallback, its 'type' field (str) doesn't conform to the expectation
# that all discriminated types define a Literal for the discriminator.

# To fix this, ensure that any type that can be an outcome of the discrimination
# has a `Literal` value for its `type` field.
# If `NarrativeEntity` is to be instantiated for types like "MacroIndicator" (before we made a class for it),
# then its `type` field needs to be able to hold those values.

# The error means: if `NarrativeEntity` is chosen by the discriminator, what `Literal` value of `type` does it correspond to?
# Since its `type` is `str`, it doesn't.
# We must ensure that only classes with `Literal` types for the discriminator field are part of the "choices"
# or that the base class itself also has a `Literal` type if it's a valid choice.

# Let's add MacroIndicator and ensure the Union is composed of types that correctly define their `type` Literal.
# The `NarrativeEntity` type `str` is the problem if it's a direct candidate.

# Solution: Modify NarrativeEntity so its `type` is also a Literal, or ensure it's abstract / not directly in the union.
# If NarrativeEntity is a fallback, it's more complex.
# For now, let's assume NarrativeEntity instances from JSON would have a specific type not covered by subclasses.
# The simplest fix to satisfy Pydantic is to give NarrativeEntity.type a Literal too.
# This implies that a "generic" entity must have one of these literal types.

# Let's define specific types and only include those in the Union.
# If a type in JSON is not one of these, it will fail parsing, which is often desired.
ConcreteEntityUnion = Annotated[Union[Company, Industry, MacroIndicator], Field(discriminator='type')]


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
