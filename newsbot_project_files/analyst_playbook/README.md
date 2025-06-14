# Analyst Playbook: Financial Research, Analysis, and Reporting

## Introduction

Welcome to the Analyst Playbook! This guide is designed to assist financial analysts, researchers, and anyone involved in understanding companies, industries, or market outlooks. It provides a walkthrough of research techniques, information gathering strategies, analysis methodologies, and reporting best practices.

This playbook covers both traditional/manual research methods and discusses how to leverage Large Language Models (LLMs) – using the provided `01_llm_prompt_library.json` and `00_main_orchestrator_prompt.md` – as powerful assistants in this process.

The goal is to help you produce comprehensive, insightful, and clearly communicated reports suitable for senior management or other key stakeholders.

---

## I. Foundational Research Techniques (Manual & Tool-Assisted)

Effective financial analysis begins with robust information gathering. Here are foundational techniques:

### 1. Defining Research Scope
Before diving in, clearly define:
*   **Subject:** Is it a specific company (e.g., Apple Inc.), an entire industry (e.g., Semiconductor Manufacturing), or a broader economic/market outlook (e.g., Impact of AI on Tech Sector)?
*   **Objective:** What questions are you trying to answer? What decisions will this research inform? (e.g., investment, competitive analysis, strategic planning).
*   **Depth & Timeline:** How detailed does the report need to be? What's the deadline? (Refer to `[Report Depth]` and `[Report Date]` placeholders if using the LLM library).
*   **Audience:** Who is this report for (e.g., CEO, investment committee, strategy team)? This dictates tone, technicality, and focus.

### 2. Utilizing Search Engines Effectively
Google, DuckDuckGo, Bing, etc., are primary tools. Go beyond simple searches:
*   **Advanced Queries:**
    *   `"exact phrase"`: For specific terms or quotes.
    *   `site:example.com keyword`: Search only within a specific website (e.g., `site:apple.com investor relations`).
    *   `filetype:pdf keyword`: Find PDF documents (often reports, presentations).
    *   `keyword OR keyword`: Broaden search.
    *   `keyword -exclude`: Exclude terms.
    *   `related:example.com`: Find sites similar to a known one.
*   **Date Filters:** Use search engine tools to filter results by time period (e.g., last month, last year, custom range) to find recent or historical information.
*   **News Tab:** Utilize the "News" tab in search engines, but always vet the sources.

### 3. Setting up News Alerts
Stay updated with automated alerts:
*   **Google Alerts (`alerts.google.com`):** Set up alerts for company names, ticker symbols, industry keywords, competitor names.
*   **Financial News Platforms:** Many platforms (e.g., Bloomberg, Reuters, specialized financial sites) offer email alerts for followed stocks or topics.
*   **Email Rules:** Create email filters/rules to organize incoming alerts.

### 4. Accessing Company Investor Relations (IR)
The most authoritative source for company-specific information:
*   **IR Website:** Usually `investor.companyname.com` or linked from their main site. Look for:
    *   **SEC Filings:** 10-K (annual), 10-Q (quarterly), 8-K (current events), Proxy Statements. These are critical.
    *   **Press Releases:** Official company announcements.
    *   **Quarterly Earnings Reports/Presentations:** Summaries of financial performance, management discussion.
    *   **Conference Call Webcasts/Transcripts:** Management discussing results and outlook with analysts.
    *   **Annual Reports:** Often more narrative and visually rich than 10-Ks.
    *   **Corporate Governance Information.**
*   **Tip:** Download key PDF filings for offline access and annotation.

### 5. Leveraging Financial News Platforms
*   **Reputable Sources:** Wall Street Journal, Financial Times, Bloomberg, Reuters, New York Times Business, The Economist, etc.
*   **Specialized Industry Publications:** Trade journals, industry-specific news sites.
*   **Subscription Services:** Many professional analysts rely on paid terminals (Bloomberg Terminal, Refinitiv Eikon) or premium news/data subscriptions. If available, these are invaluable.
*   **Be Critical:** Always consider the source's potential bias and reputation. Cross-reference information.

### 6. Using Local File Systems for Research Management
*   **Organized Folders:** Create a structured folder system for each research project (e.g., `Project_CompanyName/SEC_Filings/`, `Project_CompanyName/News_Articles/`, `Project_CompanyName/Analyst_Reports/`).
*   **Consistent Naming:** Use clear, consistent file naming conventions (e.g., `CompanyName_10Q_Q3_2023.pdf`, `ArticleSource_Headline_YYYYMMDD.pdf`).
*   **Note-Taking Tools:** Use tools like Evernote, Notion, OneNote, or simple text files to collate notes, links, and thoughts.

---

## II. Information Gathering Strategy

A systematic approach is key to avoid being overwhelmed.

1.  **Initial Broad Scan:** Start with general searches and reading recent company overview reports or news summaries to get a lay of the land.
2.  **Deep Dive into Core Areas:**
    *   **Company Profile:** Understand its business model, products/services, management, history, industry.
    *   **Financials:** Analyze trends in revenue, profitability, debt, cash flow from SEC filings and earnings reports.
    *   **News & Events:** Track significant developments, press releases, market reactions.
    *   **Industry Context:** Understand broader industry trends, competitive landscape, regulatory environment.
3.  **Organize As You Go:** Don't wait until the end. Summarize articles, extract key data points, and save documents into your organized folder structure as you find them.
4.  **Track Sources:** Maintain a list of sources (URLs, document titles, dates) for later citation. Tools like Zotero or Mendeley can help if you're doing academic-style research.

---

## III. Leveraging LLMs for Research & Analysis

Large Language Models can be powerful research and analysis assistants. The provided `01_llm_prompt_library.json` and `00_main_orchestrator_prompt.md` are designed to guide an LLM through a comprehensive financial reporting task.

### 1. Overview of Provided LLM Tools
*   **`00_main_orchestrator_prompt.md`:** This is your primary starting prompt. It instructs the LLM to follow a multi-phase approach, assess its own capabilities, and then use other specialized prompts.
*   **`01_llm_prompt_library.json`:** This file contains a structured collection of detailed prompts for each phase and sub-task (environment assessment, data gathering, analysis, reporting). The orchestrator prompt refers to these specialized prompts.

### 2. How to Use with an LLM
1.  **Start with the Orchestrator:** Copy the content of `00_main_orchestrator_prompt.md` into your chosen LLM interface.
2.  **Fill Placeholders:** Replace global placeholders like `[Company Name]`, `[Ticker Symbol]`, `[Report Date]`, `[User Name]`, and `[Report Depth]` with your specific details.
3.  **LLM Self-Assessment:** The LLM should first respond by describing its capabilities (tools, knowledge cutoff, API access like NewsBot). This is guided by the "Phase 1" section of the orchestrator, which internally uses prompts from category `2_environment_assessment`.
4.  **Guided Data Gathering & Analysis:** The orchestrator will then guide the LLM through subsequent phases. The LLM *should* conceptually refer to the specialized prompts in the library (e.g., for fetching news, performing SWOT).
    *   **Note for Human Analyst:** While the LLM is guided by the orchestrator, you, the human, can also look at the `01_llm_prompt_library.json` to understand the specific instructions being (conceptually) followed for each sub-task. You can even use these sub-prompts directly with an LLM if you want to perform only a specific part of the analysis (e.g., just a SWOT analysis).
5.  **Iterative Process:** The orchestrator suggests the LLM can provide outputs phase-by-phase. This allows you to review and guide the LLM if it goes off-track or if you want to refine a particular section.

### 3. Adapting Library Prompts
*   The templates in `01_llm_prompt_library.json` are starting points. You might need to tweak wording based on the specific LLM you are using or the nuances of your research target.
*   **JSON Output:** Many prompts are designed to ask the LLM for structured JSON output for specific data points (e.g., list of news articles, catalysts). This is very useful if you intend to process the LLM's output programmatically. Check if your LLM is good at generating valid JSON.

### 4. Providing Context to LLMs
*   **Be Specific:** The more specific your `[Company Name]`, `[Report Depth]`, and other inputs, the better the LLM's output.
*   **Tool Availability:** The framework is designed to be adaptive. If the LLM says it *doesn't* have web search or can't access a "NewsBot API", its strategy (and yours, if guiding it) will need to adjust, perhaps relying more on its pre-trained knowledge or manual data input.

---

## IV. Synthesizing Information and Report Writing

Once information is gathered (manually, via LLM, or a mix), the next step is synthesis and drafting the report.

### 1. Structuring a Financial Report
A typical structure (also suggested in the LLM's `compile_draft_report` prompt):
*   **Executive Summary:** High-level overview for senior management.
*   **Company Overview:** Who they are, what they do, their mission.
*   **Recent Developments & News Analysis:** Key events, thematic summary, sentiment.
*   **Financial Performance Review:** Key metrics, trends, comparison to peers/history.
*   **Industry & Market Context:** Relevant industry trends, competitive landscape.
*   **Strategic Analysis:** SWOT, Key Risks, Potential Catalysts.
*   **Outlook / Conclusion:** Synthesized view of future prospects.
*   **Appendix (Optional):** Detailed financial tables, list of all news articles.

### 2. Writing Tips
*   **Clarity & Conciseness:** Use clear language. Avoid jargon where possible, or explain it. Get to the point.
*   **Objectivity:** Present information factually. Clearly distinguish between facts and your analytical opinions or interpretations (or the LLM's).
*   **Storytelling:** A good report tells a story. Connect the dots between different pieces of information.
*   **Visuals (Conceptual):** Think about where charts (stock performance, financial trends) or tables would enhance understanding. The LLM can generate data for these; a human would typically create the actual visuals.

### 3. Data Verification & Citation (Crucial!)
*   **Verify Critical Data:** Especially if using an LLM, cross-reference key financial figures or impactful statements with primary sources (e.g., SEC filings, company press releases). LLMs can hallucinate or misinterpret.
*   **Cite All Sources:** Whether the report is human-written or LLM-assisted, all external sources of information, data, and direct quotes must be cited. This maintains credibility and allows readers to check sources.

---

## V. Best Practices

*   **Maintain Objectivity:** Strive for an unbiased assessment. Acknowledge both positives and negatives.
*   **Ethical Considerations:** Be mindful of insider trading regulations. Don't misrepresent information. Respect data privacy if dealing with non-public information (NPI).
*   **Continuous Learning:** Financial markets, industries, and companies are constantly evolving. Stay curious and keep learning.
*   **Understand Limitations:** Be aware of the limitations of your tools (including LLMs – knowledge cutoffs, potential for bias, hallucinations) and your own analytical biases.

---

## VI. Further Development (Connecting to NewsBot)

The `NewsBot` application (the codebase this `analyst_playbook` folder might reside with) is designed to be an AI-powered tool that automates some of the data aggregation and initial analysis described here.

**Conceptual Integration:**
*   **NewsBot as a Data Source:** A fully developed NewsBot could expose an API (as hypothesized in the LLM prompts). A human analyst or an LLM could then query this API to get:
    *   Structured company profiles.
    *   Aggregated news with pre-calculated sentiment and AI-derived categories.
    *   Formatted stock price history.
*   **Streamlining Research:** This would reduce the manual effort in basic data gathering, allowing the analyst (or LLM) to focus more on higher-level analysis, synthesis, and interpretation.
*   **Playbook & NewsBot Synergy:** This playbook would then guide the analyst on how to *use* NewsBot's output effectively, how to supplement it with other research, and how to integrate it into their final report. The LLM prompts in the library already include branches for using NewsBot API data if available.

This playbook, in conjunction with tools like the conceptual NewsBot and the provided LLM prompt library, aims to create a powerful and flexible environment for financial analysis and reporting.


---

## VII. Example Report Scenarios

To further illustrate the concepts discussed in this playbook and provide practical templates, several example report scenarios have been created. These are fictional examples designed to showcase how an analyst might structure reports for different situations, highlighting key information for escalation to senior management.

You can find these examples in the current directory:

1.  **[Negative News Report Example](./example_report_negative_news.md)**
    *   **File:** `example_report_negative_news.md`
    *   **Scenario:** Simulates a report on "Innovatech Dynamics Corp." facing a critical product safety recall. It details the event, potential impacts (financial, reputational, legal), and key information for immediate escalation.
    *   **Focus:** Rapid response to urgent negative events, impact assessment, and crisis management considerations.

2.  **[PEP Risk Assessment Example](./example_report_pep_assessment.md)**
    *   **File:** `example_report_pep_assessment.md`
    *   **Scenario:** Assesses the risks associated with "GlobalTransact Ltd." engaging a Politically Exposed Person (PEP), "Mr. Alistair Finch."
    *   **Focus:** Identification of PEP-related risks (corruption, sanctions, reputational), summary of (hypothetical) due diligence, and recommendations for mitigation and senior management review.

3.  **[Financial Snapshot & Alert Example](./example_report_financial_snapshot.md)**
    *   **File:** `example_report_financial_snapshot.md`
    *   **Scenario:** Provides a snapshot for "NextGen CyberSec Inc. (NCS)" after a significant quarterly earnings miss, covering financial performance, valuation concerns, and stock trading activity.
    *   **Focus:** Highlighting deviations from financial expectations, analyzing market reactions, and identifying key points for strategic discussion by senior management.

These examples can be used as templates or inspiration when drafting your own analytical reports for similar situations. Remember to replace all fictional details with your actual research findings.
=======
