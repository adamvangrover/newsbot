from typing import List, Optional, Dict, Any
from ..core_models.python.base_types import KnowledgeGraphData, NarrativeEntity, Driver, Relationship, Company

class SimpleReasoner:
    def __init__(self, kg_data: KnowledgeGraphData):
        self.kg_data = kg_data
        self._build_indexes()

    def _build_indexes(self):
        """Helper to build quick lookup dictionaries for entities, drivers, etc."""
        self.entities_by_id: Dict[str, NarrativeEntity] = {entity.id: entity for entity in self.kg_data.entities}
        self.drivers_by_id: Dict[str, Driver] = {driver.id: driver for driver in self.kg_data.drivers}

        self.relationships_by_source: Dict[str, List[Relationship]] = {}
        self.relationships_by_target: Dict[str, List[Relationship]] = {}

        for rel in self.kg_data.relationships:
            self.relationships_by_source.setdefault(rel.source_id, []).append(rel)
            self.relationships_by_target.setdefault(rel.target_id, []).append(rel)

    def get_entity_by_id(self, entity_id: str) -> Optional[NarrativeEntity]:
        """Retrieves an entity by its ID."""
        return self.entities_by_id.get(entity_id)

    def get_driver_by_id(self, driver_id: str) -> Optional[Driver]:
        """Retrieves a driver by its ID."""
        return self.drivers_by_id.get(driver_id)

    def get_relationships_for_entity(self, entity_id: str, direction: str = "all") -> List[Relationship]:
        """
        Retrieves relationships connected to an entity.
        Direction can be 'source' (entity is source), 'target' (entity is target), or 'all'.
        """
        rels = []
        if direction in ["source", "all"]:
            rels.extend(self.relationships_by_source.get(entity_id, []))
        if direction in ["target", "all"]:
            rels.extend(self.relationships_by_target.get(entity_id, []))

        # Deduplicate by ID to avoid issues with hashing complex objects
        unique_rels_by_id: Dict[str, Relationship] = {}
        for rel in rels:
            if rel.id not in unique_rels_by_id:
                unique_rels_by_id[rel.id] = rel
        return list(unique_rels_by_id.values())

    def find_direct_drivers_for_company(self, company_id: str) -> List[Dict[str, Any]]:
        """
        Finds drivers that directly impact a given company and provides a simple explanation.
        """
        company = self.get_entity_by_id(company_id)
        if not company or not isinstance(company, Company): # Pydantic should ensure Company type if ID is correct
             # Or check company.type == "Company" if not using discriminated unions fully
            print(f"Company with ID {company_id} not found or not a Company entity.")
            return []

        affecting_drivers_info = []

        # Relationships where the company is the target
        incoming_rels = self.relationships_by_target.get(company_id, [])

        for rel in incoming_rels:
            driver = self.get_driver_by_id(rel.source_id)
            if driver:
                explanation = f"Driver '{driver.name}' ({driver.id}) {rel.type} Company '{company.name}' ({company.id})."
                if rel.explanation_template:
                    try:
                        explanation = rel.explanation_template.format(source_name=driver.name, target_name=company.name, type=rel.type)
                    except KeyError: # Template might have other placeholders
                        pass

                affecting_drivers_info.append({
                    "driver_id": driver.id,
                    "driver_name": driver.name,
                    "relationship_type": rel.type,
                    "relationship_id": rel.id,
                    "explanation": explanation,
                    "impact_potential": driver.impact_potential,
                    "strength": rel.strength
                })
        return affecting_drivers_info

    def generate_simple_narrative_for_company_drivers(self, company_id: str) -> str:
        """
        Generates a very basic narrative string about drivers affecting a company.
        """
        company = self.get_entity_by_id(company_id)
        if not company:
            return f"No company found with ID {company_id}."

        drivers_info = self.find_direct_drivers_for_company(company_id)
        if not drivers_info:
            return f"No direct drivers found for {company.name} ({company_id})."

        narrative_parts = [f"Key drivers influencing {company.name} ({company_id}):"]
        for info in drivers_info:
            part = f"- {info['driver_name']}: {info['explanation']}"
            if info['strength']:
                part += f" (Strength: {info['strength']})"
            if info['impact_potential']:
                 part += f" (Potential Impact: {info['impact_potential']})"
            narrative_parts.append(part)

        return "\n".join(narrative_parts)


if __name__ == '__main__':
    # Example Usage (requires load_sample_data to be accessible)
    from ..data.load_sample_data import load_knowledge_graph_from_json

    kg_data = load_knowledge_graph_from_json()
    if kg_data:
        reasoner = SimpleReasoner(kg_data)

        # Test get_entity_by_id
        test_company_id = "comp_alpha"
        alpha_soft = reasoner.get_entity_by_id(test_company_id)
        if alpha_soft:
            print(f"Found entity: {alpha_soft.name}, Type: {alpha_soft.type}\n")

        # Test get_relationships_for_entity
        print(f"Relationships for {test_company_id}:")
        for rel in reasoner.get_relationships_for_entity(test_company_id):
            print(f"  {rel.id}: {rel.source_id} -> {rel.target_id} ({rel.type})")
        print("\n")

        # Test find_direct_drivers_for_company
        print(f"Direct drivers for {test_company_id} ({alpha_soft.name if alpha_soft else ''}):")
        drivers_info_alpha = reasoner.find_direct_drivers_for_company(test_company_id)
        for info in drivers_info_alpha:
            print(f"  Driver: {info['driver_name']}, Relationship: {info['relationship_type']}, Explanation: {info['explanation']}")
        print("\n")

        # Test generate_simple_narrative_for_company_drivers
        narrative_alpha = reasoner.generate_simple_narrative_for_company_drivers(test_company_id)
        print("Narrative for AlphaSoft Inc.:")
        print(narrative_alpha)
        print("\n")

        test_beta_id = "comp_beta"
        narrative_beta = reasoner.generate_simple_narrative_for_company_drivers(test_beta_id)
        print("Narrative for BetaDrive Motors:")
        print(narrative_beta)
        print("\n")

        # Test with a non-existent company
        narrative_fake = reasoner.generate_simple_narrative_for_company_drivers("fake_comp")
        print(narrative_fake)

    else:
        print("Could not load knowledge graph data for reasoner example.")
