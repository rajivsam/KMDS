# Design Rationale (Simplified)

KMDS is easiest to maintain when treated as a small core library with optional integrations.

## Core Product Goal

Capture workflow observations in a consistent ontology-backed format and load them back for reporting.

## Keep in Scope (Core)

1. Ontology model and workflow/observation classes
2. Observation loading utilities and tabular outputs
3. Stable path/config helpers needed by tests and examples
4. Search capabilities over project knowledge bases:
	1. Semantic index creation from RDF-backed observations
	2. Programmatic semantic search API
	3. Optional natural-language routing over predefined search templates

## Keep Out of Core (Optional)

1. Cloud storage connectors (Box/MinIO)
2. Prefect pipeline examples
3. LLM/report-generation guidance

These can stay in the repository as examples, but should not be required to understand or run the core KMDS package.

## Search Features Added

The search subsystem now includes two complementary capabilities.

1. Semantic index and vector search
	1. Observation text is embedded and indexed in ChromaDB.
	2. Users can query a project knowledge base with natural language and retrieve semantically similar findings.
	3. This provides robust retrieval even when query wording differs from the original notes.
2. LLM search orchestrator
	1. A router maps free-form user questions to predefined KMDS search templates.
	2. Routing output is schema-constrained using Pydantic to keep tool arguments valid and predictable.
	3. Tool descriptions are injected into prompts so the model knows available template choices.
	4. If routing fails or no template matches, the system falls back to semantic vector search.
	5. Results are synthesized into concise natural-language answers and also returned as raw records.
3. User-facing interfaces
	1. Python API for programmatic use in notebooks and scripts.
	2. CLI entry points for reproducible command-line workflows.

## Why This Helps the KMDS User Community

1. Lowers adoption barriers
	1. New users can ask plain-language questions without learning ontology internals first.
	2. Teams can use CLI and API paths that fit both ad hoc and production workflows.
2. Improves discoverability of prior work
	1. Semantic retrieval makes previously captured observations easier to find across project phases.
	2. Router-based template matching directs users toward phase-specific evidence when available.
3. Increases trust and reproducibility
	1. Pydantic-validated routing reduces malformed tool invocations.
	2. Deterministic fallback behavior ensures users still get useful results when LLM routing is uncertain.
	3. Raw records remain inspectable, so generated summaries can be verified.
4. Balances capability with maintainability
	1. The current design avoids unnecessary framework coupling while delivering practical search value now.
	2. Architecture remains open to future adapter-based integrations if community needs evolve.

## Related Design Documents

1. Development context: [knowledge_management_in_DS.md](knowledge_management_in_DS.md)
2. Workflow recipe: [km_app_pipeline.md](km_app_pipeline.md)
3. Ontology rationale: [ontology_management.md](ontology_management.md)
4. Observation glossary: [glossary_observation_types.md](glossary_observation_types.md)