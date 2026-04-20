[0.3.2]
* Added natural language observation ingestion feature. Given a free-form text statement, KMDS classifies it into the matching KMDS ontology observation type, extracts structured entities (metric, value, timestamp, affected component), validates the input, and either returns a structured summary or logs the observation to a KMDS knowledge base.
* Added two interaction modes: summary mode returns a classification and entity extraction result without modifying any file; log mode creates or updates a KMDS knowledge base and appends the observation.
* Added JSON-LD and Python logging-code generation from mapped observations.
* Added a new CLI command, kmds-observe, for natural-language observation ingestion with text, JSON, and text-file input modes.
* Added a dedicated documentation page covering all interaction modes including Python API, JSON-LD, Python code generation, CLI summary, and CLI log modes.
* Updated README to reflect a broader user audience: data scientists, software developers, and business analysts who know Python.
* Updated concepts documentation with a natural language ingestion section and a user-audience framing section.
* Updated analytics and machine learning EDA phase example notebooks to show one observation created via the natural language mapper.
* Updated analytics and machine learning observations report notebooks with a natural language ingestion section showing summary mode, mapping mode, and a commented log-mode example.

[0.3.1]
* Added semantic indexing for KMDS project knowledge bases, using sentence-transformer embeddings with a ChromaDB vector store for natural-language retrieval.
* Added an LLM-based search orchestrator that routes user questions to predefined KMDS search templates, validates routing arguments with Pydantic schemas, and synthesizes concise answers from raw results.
* Added deterministic fallback logic in the orchestrator to semantic vector search when routing is invalid, unmatched, or returns no structured results.
* Added context injection for routing prompts via explicit template/tool descriptions so the LLM can choose from known KMDS search options.
* Added a new CLI command, kmds-ask, for natural-language project search with text and JSON output modes.
* Added documentation for natural-language search orchestration and updated module/index docs to include the new search components.
* Added and validated orchestrator-focused tests, with full suite passing.

[0.0.2.8]
* Standardized path and file utils for use with both repository and cloud endpoints
* Read the docs documentation for KMDS generated.


[0.0.2.9]
* Wiki page on design perspective added
* Examples for Minio based file read and write added. Docker files added.
* Examples of generating semantic meta-data for clean data represenations that are used for modelling is illustrated with woodwork.

[0.0.3.0]
* Removed cloud features and packages related to documenting meta-data for datasets, these can be captured by code generation tools now
* Refactored examples to illustrate the use of generative AI in data science and or data analysis projects
* Created better example documentation using generative AI tools.
