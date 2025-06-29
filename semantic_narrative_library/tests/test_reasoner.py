import pytest
from pathlib import Path

from ..core_models.python.base_types import KnowledgeGraphData, Company
from ..reasoning_engine.simple_reasoner import SimpleReasoner
from ..data.load_sample_data import load_knowledge_graph_from_json, DEFAULT_DATA_PATH

# Fixture to load KG data and initialize reasoner once per test session (or module)
@pytest.fixture(scope="module")
def reasoner_instance() -> SimpleReasoner:
    """Loads KG data and returns an initialized SimpleReasoner instance."""
    # For tests, always use the default sample data path to ensure consistency
    kg_data = load_knowledge_graph_from_json(DEFAULT_DATA_PATH)
    if not kg_data:
        pytest.fail("Failed to load sample knowledge graph data for testing.")
    return SimpleReasoner(kg_data)

def test_get_entity_by_id(reasoner_instance: SimpleReasoner):
    """Test retrieving entities by ID."""
    # Test existing company
    comp_alpha = reasoner_instance.get_entity_by_id("comp_alpha")
    assert comp_alpha is not None
    assert comp_alpha.name == "AlphaSoft Inc."
    assert isinstance(comp_alpha, Company) # Due to discriminated union

    # Test existing industry
    ind_tech = reasoner_instance.get_entity_by_id("ind_tech")
    assert ind_tech is not None
    assert ind_tech.name == "Technology Software"
    assert ind_tech.type == "Industry"

    # Test non-existent entity
    non_existent = reasoner_instance.get_entity_by_id("fake_id_123")
    assert non_existent is None

def test_get_driver_by_id(reasoner_instance: SimpleReasoner):
    """Test retrieving drivers by ID."""
    driver_cloud = reasoner_instance.get_driver_by_id("drv_cloud_adoption")
    assert driver_cloud is not None
    assert driver_cloud.name == "Cloud Computing Adoption"

    non_existent_driver = reasoner_instance.get_driver_by_id("fake_driver_id")
    assert non_existent_driver is None

def test_get_relationships_for_entity(reasoner_instance: SimpleReasoner):
    """Test retrieving relationships for a given entity."""
    comp_alpha_rels = reasoner_instance.get_relationships_for_entity("comp_alpha")
    assert len(comp_alpha_rels) == 3 # belongs_to_industry, positively_impacts, pressures_valuation_of

    rel_ids_for_comp_alpha = {rel.id for rel in comp_alpha_rels}
    expected_rel_ids = {"rel_asft_industry", "rel_cloud_asft", "rel_interest_asft_valuation"}
    assert rel_ids_for_comp_alpha == expected_rel_ids

    # Test relationships where comp_alpha is source
    comp_alpha_source_rels = reasoner_instance.get_relationships_for_entity("comp_alpha", direction="source")
    assert len(comp_alpha_source_rels) == 1
    assert comp_alpha_source_rels[0].id == "rel_asft_industry"

    # Test relationships where comp_alpha is target
    comp_alpha_target_rels = reasoner_instance.get_relationships_for_entity("comp_alpha", direction="target")
    assert len(comp_alpha_target_rels) == 2
    target_rel_ids = {rel.id for rel in comp_alpha_target_rels}
    expected_target_rel_ids = {"rel_cloud_asft", "rel_interest_asft_valuation"}
    assert target_rel_ids == expected_target_rel_ids


def test_find_direct_drivers_for_company(reasoner_instance: SimpleReasoner):
    """Test finding direct drivers for a company."""
    comp_alpha_drivers_info = reasoner_instance.find_direct_drivers_for_company("comp_alpha")
    assert len(comp_alpha_drivers_info) == 2

    driver_names = {info["driver_name"] for info in comp_alpha_drivers_info}
    assert "Cloud Computing Adoption" in driver_names
    assert "Interest Rate Hikes" in driver_names

    # Check structure of one of the driver info dicts
    cloud_driver_info = next(d for d in comp_alpha_drivers_info if d["driver_id"] == "drv_cloud_adoption")
    assert cloud_driver_info["relationship_type"] == "positively_impacts"
    assert cloud_driver_info["explanation"] == "Cloud Computing Adoption significantly benefits AlphaSoft Inc. due to its strong cloud portfolio."

    # Test with a company that has no direct drivers defined (if any in sample, or add one)
    # For now, let's test a non-company ID
    not_a_company_drivers = reasoner_instance.find_direct_drivers_for_company("ind_tech")
    assert not_a_company_drivers == [] # Expect empty list as it's not a company

    non_existent_company_drivers = reasoner_instance.find_direct_drivers_for_company("fake_comp_id")
    assert non_existent_company_drivers == []


def test_generate_simple_narrative_for_company_drivers(reasoner_instance: SimpleReasoner):
    """Test generating the simple narrative for a company."""
    narrative_alpha = reasoner_instance.generate_simple_narrative_for_company_drivers("comp_alpha")
    assert "Key drivers influencing AlphaSoft Inc. (comp_alpha):" in narrative_alpha
    assert "Cloud Computing Adoption" in narrative_alpha
    assert "Interest Rate Hikes" in narrative_alpha

    narrative_fake = reasoner_instance.generate_simple_narrative_for_company_drivers("fake_comp_id")
    assert "No company found with ID fake_comp_id." in narrative_fake

    narrative_not_company = reasoner_instance.generate_simple_narrative_for_company_drivers("ind_tech")
    # This will print "Company with ID ind_tech not found or not a Company entity." inside find_direct_drivers_for_company
    # and then "No direct drivers found for Technology Software (ind_tech)."
    assert "No direct drivers found for Technology Software (ind_tech)." in narrative_not_company

# To run: From repository root: python -m pytest semantic_narrative_library/tests/test_reasoner.py
# Or simply: python -m pytest semantic_narrative_library/tests
# (if __init__.py files are correctly set up for package discovery)
