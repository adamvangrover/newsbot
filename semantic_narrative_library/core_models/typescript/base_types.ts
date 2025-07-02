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

export interface MacroIndicator extends NarrativeEntity {
  type: 'MacroIndicator'; // Literal type for discrimination
  region?: string;
}

export interface NewsItem extends NarrativeEntity {
  type: 'NewsItem';
  source_name?: string; // e.g., Reuters, Bloomberg
  url?: string;
  publication_date?: string; // ISO date string
  sentiment_score?: number; // e.g., -1.0 to 1.0
  key_entities_mentioned_ids?: string[];
  summary?: string;
}

export interface PoliticalEvent extends NarrativeEntity {
  type: 'PoliticalEvent';
  location?: string;
  event_date?: string; // ISO date string
  event_subtype?: string; // e.g., Election, Protest, TradeDealAnnouncement
  involved_parties?: string[];
  perceived_impact_area?: string;
}

export interface FinancialReportItem extends NarrativeEntity {
  type: 'FinancialReportItem';
  company_id: string;
  report_type: "10-K" | "10-Q" | "8-K" | "Annual Report" | "Quarterly Report" | "Other";
  period_ending_date?: string; // ISO date string
  filing_date?: string; // ISO date string
  key_metrics?: Record<string, any>; // e.g., {'Revenue': 100M, 'NetIncome': 10M}
  link_to_report?: string;
}

export interface MarketSignal extends NarrativeEntity {
  type: 'MarketSignal';
  signal_type: string; // e.g., "PriceSpike", "VolumeSurge"
  asset_class?: string;
  security_id?: string; // Link to a Security entity
  timestamp: string; // ISO date string
  details?: Record<string, any>;
}

export interface RegulatoryChange extends NarrativeEntity {
  type: 'RegulatoryChange';
  jurisdiction: string;
  agency?: string;
  status: "Proposed" | "Enacted" | "Repealed" | "Guidance";
  summary: string;
  effective_date?: string; // ISO date string
  industries_affected_ids?: string[];
}

export interface Security extends NarrativeEntity {
  type: 'Security';
  issuer_id?: string; // ID of the issuing Company or entity
  security_subtype: string; // E.g., "CommonStock", "CorporateBond"
  ticker?: string;
  cusip?: string;
  isin?: string;
  exchange?: string;
}


// Union type for all concrete entity types for use in KnowledgeGraphData.entities
export type AnyConcreteEntity =
  | Company
  | Industry
  | MacroIndicator
  | NewsItem
  | PoliticalEvent
  | FinancialReportItem
  | MarketSignal
  | RegulatoryChange
  | Security;
  // Add other concrete types here. NarrativeEntity itself is the base.

// This will be the core of our knowledge graph, likely a collection of entities and relationships
export interface KnowledgeGraphData {
  entities: AnyConcreteEntity[]; // Use the union of specific types
  drivers: Driver[];
  relationships: Relationship[];
  semanticLinks?: SemanticLink[];
}
