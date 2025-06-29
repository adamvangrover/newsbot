// Basic Interfaces for the Semantic Narrative Library

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
  impactPotential?: 'High' | 'Medium' | 'Low' | string; // Allow string for custom values
  // Example: How this driver typically influences things
  influencePattern?: string;
  // Entities this driver is commonly associated with
  relatedEntityTypes?: string[];
  tags?: string[];
}

export interface Relationship {
  id: string;
  sourceId: string; // ID of the source NarrativeEntity or Driver
  targetId: string; // ID of the target NarrativeEntity or Driver
  type: string; // e.g., "influences", "owns", "competes_with", "is_part_of", "has_driver"
  strength?: number; // e.g., 0.0 to 1.0
  direction?: 'unidirectional' | 'bidirectional';
  explanationTemplate?: string; // e.g., "{sourceName} {type} {targetName}"
  attributes?: Record<string, any>;
  tags?: string[];
}

export interface SemanticLink {
  id: string;
  // ID of the element being linked (e.g., a specific Driver instance affecting a Company, or a generated narrative)
  narrativeElementId: string;
  metricObserved: string; // e.g., "StockPrice", "AnalystRating", "SentimentScore"
  // Could be a specific value, a range, or a qualitative observation
  observedValue?: string | number | [number, number];
  observationTime?: Date;
  sourceOfObservation?: string; // Where this link was derived from
  confidence?: number; // e.g., 0.0 to 1.0
  explanation: string; // Why this link/observation is relevant
  tags?: string[];
}

// Example of a more specific entity type
export interface Company extends NarrativeEntity {
  type: 'Company';
  tickerSymbol?: string;
  industryId?: string;
  country?: string;
}

export interface Industry extends NarrativeEntity {
  type: 'Industry';
  sector?: string;
}

// This will be the core of our knowledge graph, likely a collection of entities and relationships
export interface KnowledgeGraphData {
  entities: NarrativeEntity[];
  drivers: Driver[];
  relationships: Relationship[];
  semanticLinks?: SemanticLink[];
}
