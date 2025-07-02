package com.example.narrativelibrary.model;

import java.util.List;
import java.util.Map;
import java.util.Date;

// Using a single file for brevity in this initial setup.
// In a full project, these would be separate .java files.

public class BaseTypes {

    public static class NarrativeEntity {
        public String id;
        public String name;
        public String description;
        public String type; // e.g., "Industry", "Company", "MacroIndicator"
        public Map<String, Object> attributes;
        public List<String> tags;

        // Constructors, getters, setters would go here
    }

    public static class Driver {
        public String id;
        public String name;
        public String description;
        public String impactPotential; // "High", "Medium", "Low", or custom
        public String influencePattern;
        public List<String> relatedEntityTypes;
        public List<String> tags;

        // Constructors, getters, setters
    }

    public static class Relationship {
        public String id;
        public String sourceId;
        public String targetId;
        public String type; // e.g., "influences", "owns", "competes_with"
        public Double strength; // e.g., 0.0 to 1.0
        public String direction; // "unidirectional", "bidirectional"
        public String explanationTemplate;
        public Map<String, Object> attributes;
        public List<String> tags;

        // Constructors, getters, setters
    }

    public static class SemanticLink {
        public String id;
        public String narrativeElementId;
        public String metricObserved; // e.g., "StockPrice", "AnalystRating"
        public Object observedValue; // String, Number, or a custom class for ranges
        public Date observationTime;
        public String sourceOfObservation;
        public Double confidence; // e.g., 0.0 to 1.0
        public String explanation;
        public List<String> tags;

        // Constructors, getters, setters
    }

    public static class Company extends NarrativeEntity {
        // type is implicitly "Company"
        public String tickerSymbol;
        public String industryId;
        public String country;

        public Company() {
            this.type = "Company";
        }
        // Constructors, getters, setters
    }

    public static class Industry extends NarrativeEntity {
        // type is implicitly "Industry"
        public String sector;

        public Industry() {
            this.type = "Industry";
        }
        // Constructors, getters, setters
    }

    public static class KnowledgeGraphData {
        public List<NarrativeEntity> entities;
        public List<Driver> drivers;
        public List<Relationship> relationships;
        public List<SemanticLink> semanticLinks;

        // Constructors, getters, setters
    }
}
