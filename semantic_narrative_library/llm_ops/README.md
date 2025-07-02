# LLM Operations (LLMOps) for Semantic Narrative Library

This directory contains artifacts and scripts related to integrating Large Language Models (LLMs) into the Semantic Narrative Library.

## Components:

-   **`prompts/`**: Stores prompt templates used for interacting with LLMs.
    -   `company_narrative_prompt.md`: An example prompt template for generating company-specific narratives based on structured driver data.
-   **`narrative_generator.py`**: A Python script demonstrating how to:
    -   Load prompt templates.
    -   Fill prompts with dynamic data (e.g., from the `SimpleReasoner`).
    -   Simulate an LLM call to generate narratives. In a real implementation, this script would be extended to make actual API calls to an LLM service.

## Workflow:

1.  **Data Collection:** Structured data (e.g., company details, identified drivers, relationships) is gathered by the `SimpleReasoner`.
2.  **Prompt Engineering:** A suitable prompt template is selected and filled with the collected structured data.
3.  **LLM Interaction:** The filled prompt is sent to an LLM.
    -   *(Current Implementation)*: `narrative_generator.py` simulates this step with a template-based response.
    -   *(Future Implementation)*: This would involve API calls to services like OpenAI, Anthropic, Azure OpenAI, or locally hosted models.
4.  **Narrative Output:** The LLM's response (the generated narrative) is received and can be used by the system (e.g., displayed in the UI, included in reports).

## API Key Management for Real LLM Integration:

When integrating with actual LLM APIs, secure management of API keys is paramount. Keys should **never** be hardcoded. Recommended practices include:

1.  **Environment Variables:** Store API keys in environment variables (e.g., `OPENAI_API_KEY`). The application reads these at runtime.
    -   Example: `api_key = os.getenv("LLM_PROVIDER_API_KEY")`
2.  **.env Files (for Development):**
    -   Use `.env` files (e.g., `semantic_narrative_library/.env`) to store keys locally during development.
    -   Ensure `.env` is listed in your project's `.gitignore` file to prevent accidental commits.
    -   Provide a `.env.example` file in the repository, showing the required variable names without their values.
    -   Libraries like `python-dotenv` can automatically load variables from `.env` files.
3.  **Secrets Management Systems (for Production/Staging):**
    -   Utilize dedicated secrets management tools like HashiCorp Vault, AWS Secrets Manager, Google Cloud Secret Manager, or Azure Key Vault. These systems securely store and manage access to secrets, injecting them into the application environment when needed.
4.  **Restricted Permissions:** If your LLM provider supports it, create API keys with the minimum necessary permissions (e.g., access only to specific models, read-only access if applicable).

## Future Considerations for LLMOps:

-   **Model Versioning:** Tracking which LLM model versions are used.
-   **Prompt Versioning & Management:** More sophisticated systems for managing, versioning, and A/B testing prompts.
-   **Monitoring & Logging:** Logging LLM inputs, outputs, and performance metrics.
-   **Fine-tuning & Custom Models:** Processes for fine-tuning models on domain-specific data.
-   **Cost Management:** Tracking API usage and costs.
-   **Output Validation & Guardrails:** Implementing checks to ensure LLM outputs are safe, relevant, and factually grounded (to the extent possible).

This setup provides a basic framework for LLM integration, focusing on the generation of narratives from structured data.
