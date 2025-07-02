import pytest
from pydantic import ValidationError

# Assuming the test runner is started from the repository root or semantic_narrative_library's parent
# and PYTHONPATH includes the parent of semantic_narrative_library
from ..core_models.python.base_types import (
    NarrativeEntity,
    Driver,
    Relationship,
    SemanticLink,
    Company,
    Industry,
    MacroIndicator,
    KnowledgeGraphData
)

def test_narrative_entity_creation():
    """Test basic NarrativeEntity creation."""
    entity_data = {"id": "e1", "name": "Test Entity", "type": "Generic"}
    entity = NarrativeEntity(**entity_data)
    assert entity.id == "e1"
    assert entity.name == "Test Entity"
    assert entity.type == "Generic"
    assert entity.attributes == {} # Default factory
    assert entity.tags == []      # Default factory

def test_company_creation_and_type():
    """Test Company creation and its specific 'type' literal."""
    company_data = {"id": "c1", "name": "TestCo", "type": "Company", "ticker_symbol": "TST"}
    company = Company(**company_data)
    assert company.id == "c1"
    assert company.name == "TestCo"
    assert company.type == "Company" # Validated by Literal
    assert company.ticker_symbol == "TST"

    # Test that a wrong type for Company raises ValidationError
    with pytest.raises(ValidationError):
        Company(id="c2", name="WrongTypeCo", type="NotACompany")

def test_industry_creation():
    """Test Industry creation."""
    industry_data = {"id": "i1", "name": "TestInd", "type": "Industry", "sector": "Tech"}
    industry = Industry(**industry_data)
    assert industry.id == "i1"
    assert industry.sector == "Tech"
    assert industry.type == "Industry"

def test_macro_indicator_creation():
    """Test MacroIndicator creation."""
    macro_data = {"id": "m1", "name": "Interest Rate", "type": "MacroIndicator", "region": "Global"}
    indicator = MacroIndicator(**macro_data)
    assert indicator.id == "m1"
    assert indicator.region == "Global"
    assert indicator.type == "MacroIndicator"

def test_driver_creation():
    """Test Driver creation."""
    driver_data = {"id": "d1", "name": "Tech Adoption", "description": "Rate of tech adoption"}
    driver = Driver(**driver_data)
    assert driver.id == "d1"
    assert driver.description == "Rate of tech adoption"

def test_relationship_creation():
    """Test Relationship creation."""
    rel_data = {"id": "r1", "source_id": "c1", "target_id": "d1", "type": "influenced_by"}
    relationship = Relationship(**rel_data)
    assert relationship.id == "r1"
    assert relationship.source_id == "c1"
    assert relationship.target_id == "d1"
    assert relationship.type == "influenced_by"

def test_semantic_link_creation():
    """Test SemanticLink creation."""
    slink_data = {
        "id": "sl1",
        "narrative_element_id": "r1",
        "metric_observed": "StockPrice",
        "explanation": "Tech adoption positively influences stock price."
    }
    slink = SemanticLink(**slink_data)
    assert slink.id == "sl1"
    assert slink.metric_observed == "StockPrice"

def test_knowledge_graph_data_discriminated_union():
    """Test that KnowledgeGraphData correctly parses entities into specific types."""
    kg_json_data = {
        "entities": [
            {"id": "comp1", "name": "Alpha Corp", "type": "Company", "ticker_symbol": "ACRP"},
            {"id": "ind1", "name": "Software", "type": "Industry", "sector": "Technology"},
            {"id": "macro1", "name": "GDP Growth", "type": "MacroIndicator", "region": "US"},
            # This generic entity will not parse with ConcreteEntityUnion if its type isn't one of the Literals
            # For ConcreteEntityUnion, this would raise an error.
            # If EntityUnion included NarrativeEntity with type:str, it might parse as NarrativeEntity
            # Let's test with an entity that matches one of the ConcreteEntityUnion types
        ],
        "drivers": [],
        "relationships": []
    }
    kg_data = KnowledgeGraphData(**kg_json_data)
    assert len(kg_data.entities) == 3
    assert isinstance(kg_data.entities[0], Company)
    assert kg_data.entities[0].ticker_symbol == "ACRP"
    assert isinstance(kg_data.entities[1], Industry)
    assert kg_data.entities[1].sector == "Technology"
    assert isinstance(kg_data.entities[2], MacroIndicator)
    assert kg_data.entities[2].region == "US"

def test_knowledge_graph_data_invalid_entity_type():
    """Test KG data with an entity type not in ConcreteEntityUnion."""
    kg_json_data_invalid = {
        "entities": [
            {"id": "e_invalid", "name": "Invalid Entity", "type": "UnknownType"}
        ]
    }
    with pytest.raises(ValidationError):
        KnowledgeGraphData(**kg_json_data_invalid)

# To run these tests:
# 1. Navigate to the repository root (parent of semantic_narrative_library).
# 2. Run: python -m pytest semantic_narrative_library/tests
# Or, if semantic_narrative_library is in PYTHONPATH: pytest semantic_narrative_library/tests
# Or, from within semantic_narrative_library dir: python -m pytest tests/
# (Pytest should discover tests if run from parent directory of the library)
