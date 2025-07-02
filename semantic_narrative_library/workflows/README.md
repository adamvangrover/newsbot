# Workflow and Template Engine (Conceptual Design)

This directory outlines the conceptual design for a workflow and template engine within the Semantic Narrative Library. Such an engine would enable the definition and execution of complex analytical processes, including those involving impact analysis, scenario modeling, and news processing.

## Core Concepts

1.  **Workflow Template (`workflow_template_example.json`)**:
    *   Defines a sequence of processing steps or stages for a specific analytical goal (e.g., "Assess Impact of News Item on a Company's Stock Outlook").
    *   Each step would specify:
        *   `name`: A human-readable name for the step.
        *   `description`: What the step does.
        *   `component`: The processing component to execute (e.g., "NLProcessor", "SignificanceScorer", "ImpactAnalyzer", "NarrativeGenerator").
        *   `method`: The specific method of the component to call.
        *   `inputs`: How to map data from previous steps or initial parameters to the inputs of this step's method. This could involve referencing outputs of prior steps by name.
        *   `parameters`: Static parameters for the method.
        *   `outputs`: Names for the outputs of this step, which can be referenced by subsequent steps.
        *   `ruleset_id` (optional): Reference to a set of rules to be used by components like the `ImpactAnalyzer`.
    *   Workflows could support conditional logic (e.g., "if sentiment score > X, then proceed to step Y") and looping, though this adds complexity.

2.  **Rule Template (`rule_template_example.json`)**:
    *   Defines specific rules for components like the `ImpactAnalyzer` or `ScenarioModeler`.
    *   Rules would typically define cause-and-effect relationships, often with associated probabilities, magnitudes, and conditions.
    *   Example rule for impact analysis:
        *   `trigger`: A specific event or condition (e.g., `PoliticalEvent` of type `TradeRestriction` in `RegionX` affecting `IndustryY`).
        *   `impacts`: A list of potential first, second, or third-order impacts.
            *   `order`: 1st, 2nd, 3rd.
            *   `target_entity_type_selector`: Criteria to select target entities (e.g., `Company` in `IndustryY` with `exposure_to_regionX > 0.5`).
            *   `impact_type`: The nature of the impact (e.g., `SupplyChainDisruption`, `IncreasedCosts`, `ReducedSales`).
            *   `probability`: Estimated probability of this impact occurring (0.0 to 1.0).
            *   `magnitude`: Estimated magnitude (e.g., qualitative like "Low", "Medium", "High", or quantitative if possible).
            *   `timescale`: Estimated time for the impact to manifest (e.g., "Short-term", "Medium-term").
            *   `explanation_template`: A template to explain why this impact occurs.
    *   Rules could be grouped into `Rulesets` referenced by workflows.

3.  **Workflow Execution Engine (Conceptual Component)**:
    *   A Python component (not built in this scaffolding phase) responsible for:
        *   Loading a workflow template.
        *   Instantiating necessary processing components (`NLProcessor`, `ImpactAnalyzer`, etc.).
        *   Executing the steps in the defined order, passing data between them.
        *   Managing the state of a workflow instance.
        *   Handling errors and potentially logging execution details.

## Benefits

-   **Flexibility:** Allows defining various analytical processes without hardcoding them.
-   **Reusability:** Workflow and rule templates can be reused and adapted.
-   **Transparency:** The defined workflow and rules make the analytical process more understandable.
-   **Extensibility:** New processing components, steps, and rule types can be added over time.

## Current Status

-   This is a **conceptual design**. No functional workflow execution engine or rule engine is implemented in the current scaffolding.
-   Example JSON files (`workflow_template_example.json`, `rule_template_example.json`) are provided in this directory to illustrate the proposed structure.
-   The placeholder processing components in `semantic_narrative_library/processing/` would be the building blocks called by such an engine.

This design aims to provide a structured way to think about automating more complex analytical tasks within the Semantic Narrative Library. The actual implementation would be a significant undertaking.
