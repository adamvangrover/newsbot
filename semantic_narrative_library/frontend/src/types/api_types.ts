// Basic Interfaces for the Semantic Narrative Library (Frontend)
// These types should ideally match the backend Pydantic models' structure.
// Copied and adapted from core_models/typescript/base_types.ts

export interface NarrativeEntity {
  id: string;
  name: string;
  description?: string;
  type: string; // e.g., "Industry", "Company", "MacroIndicator"
  attributes?: Record<string, any>; // Flexible key-value store
  tags?: string[]; // For categorization and search
}

export interface Driver {
  id: string;
  name: string;
  description: string;
  impact_potential?: 'High' | 'Medium' | 'Low' | string; // Matches Python model
  influence_pattern?: string;
  related_entity_types?: string[];
  tags?: string[];
}

export interface Relationship {
  id: string;
  source_id: string;
  target_id: string;
  type: string;
  strength?: number;
  direction?: 'unidirectional' | 'bidirectional';
  explanation_template?: string;
  attributes?: Record<string, any>;
  tags?: string[];
}

export interface SemanticLink {
  id: string;
  narrative_element_id: string;
  metric_observed: string;
  observed_value?: string | number | [number, number]; // Matches Python model
  observation_time?: string; // Date will be string from JSON
  source_of_observation?: string;
  confidence?: number;
  explanation: string;
  tags?: string[];
}

// Specific entity types matching backend Pydantic models
export interface Company extends NarrativeEntity {
  type: 'Company'; // Literal type for discrimination
  ticker_symbol?: string;
  industry_id?: string;
  country?: string;
}

export interface Industry extends NarrativeEntity {
  type: 'Industry'; // Literal type for discrimination
  sector?: string;
}

export interface MacroIndicator extends NarrativeEntity {
  type: 'MacroIndicator'; // Literal type for discrimination
  region?: string;
  // Add other specific fields as defined in Python MacroIndicator model if any
}

// Union type for entities that can be fetched, matching ConcreteEntityUnion in Python
export type AnyEntity = Company | Industry | MacroIndicator | NarrativeEntity; // NarrativeEntity as fallback for broader typing if needed

// For API responses that return lists of drivers with explanations
export interface CompanyDriverInfo {
    driver_id: string;
    driver_name: string;
    relationship_type: string;
    relationship_id: string;
    explanation: string;
    impact_potential?: string | number;
    strength?: number;
}

// For API response for /knowledge_graph/stats
export interface KGStats {
    num_entities: number;
    num_drivers: number;
    num_relationships: number;
    num_semantic_links: number;
}
