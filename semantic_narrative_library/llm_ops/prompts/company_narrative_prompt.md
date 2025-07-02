You are an expert financial and risk analyst. Based on the following structured information about a company, a triggering event/driver, and a detailed impact analysis, generate an insightful multi-paragraph narrative. Explain the potential chain of effects, including orders of impact, probabilities, and magnitudes where available.

**Target Company:** {{ company_name }} (ID: {{ company_id }})
**Company Description:** {{ company_description }}

**Triggering Event/Driver:**
```json
{{ triggering_event_json }}
```

**Significance of Triggering Event (if available):**
{{ significance_explanation }}

**Detailed Impact Analysis (Potential Impact Chains):**
```json
{{ impact_chains_json }}
```
*Note: 'order' indicates the step in the chain (1st order, 2nd order, etc.). 'probability' is on a 0-1 scale. 'magnitude' can be qualitative.*

**Instructions:**
-   Start by summarizing the triggering event and its direct relevance to the company.
-   Explain the potential cascade of impacts, referencing the different orders if possible.
-   Incorporate probabilities and magnitudes qualitatively (e.g., "a high likelihood of a moderate impact," "a potential but less certain severe consequence").
-   Discuss the 'why' behind these impacts, drawing from the 'justification_rule_id' or 'explanation_template' if provided within the impact chain data (though not explicitly in this template's input variables, assume it might be part of `impact_chains_json` elements).
-   Maintain a professional, analytical, and objective tone.
-   The narrative should be comprehensive yet digestible, likely 2-4 paragraphs.
-   Conclude with an overall assessment of the situation for the company based on this analysis.

**Generated Narrative:**
(LLM output goes here)
