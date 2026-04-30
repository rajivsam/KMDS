# KMDS Business Value Summary

> **Knowledge Management for Data Science (KMDS)** — transforms the invisible, accumulating debt of undocumented data science work into a searchable, shareable, and auditable project record.

---

## The Core Problem: Knowledge Evaporation

Data science work is deeply iterative. An analyst moves through exploration, data preparation, modelling approach selection, and model tuning — each step producing insights and decisions that depend on the steps before. But the decisions themselves — *why this transformation, why this model, why this cutoff* — are rarely captured in any formal way.

The result is **knowledge evaporation**: the rationale behind a project is held in the analyst's head or buried in notebook comments. When the project is revisited six months later, handed to a new team member, or audited, the research trail has gone cold. The cost is not just the time spent rediscovering — it is the risk of repeating mistakes, drifting from earlier validated assumptions, or being unable to explain a model's behaviour to a stakeholder.

This is not a tooling gap in the usual sense. Most teams already have version control for code. What they lack is a structured way to record the *narrative of reasoning* alongside the code.

---

## What KMDS Does

KMDS provides a lightweight, ontology-backed knowledge base for data science workflows. It gives a team a shared place to record, load, search, and communicate findings — without requiring everyone to understand RDF or ontology engineering.

| What a team does today (without KMDS) | What KMDS provides instead |
|---|---|
| Findings documented in free-text notebook cells or comments | Structured observations logged against a typed schema (exploratory, data representation, modelling choice, model selection) |
| Decision rationale in Slack threads or email | Persisted, searchable RDF knowledge base per project |
| Onboarding a new analyst = reading dozens of notebooks | New team member asks `kmds-ask --kb project.xml --query "Why was this model chosen?"` |
| Exec summary written from scratch before a review | `kmds-exec-summary` generates a non-technical summary from the captured record |
| Analyst must know Python/ontology to log a finding | Natural-language ingestion (`kmds-observe`) and summary-log CLI work without ontology knowledge |
| Search by keyword across notebooks = grep or manual review | Semantic vector search returns semantically related findings even when wording differs |

---

## Where KMDS Adds the Most Value

### 1. Continuity across time and team changes

The highest-leverage case for KMDS is a project that lives longer than a single sprint, or changes hands. A structured, versioned knowledge base means the reasoning trail does not die with the original analyst. A new team member can query the KB in plain English and receive a synthesised answer drawn from what was actually observed — not from what can be reconstructed from code.

### 2. Non-developer access to project knowledge

The `kmds-observe`, `kmds-summary-log`, and `kmds-exec-summary` CLI tools lower the access threshold dramatically. A business analyst or project manager can log findings, run a summary query, or request an executive summary without ever opening a notebook. This reduces the bottleneck where a single technical person is responsible for all documentation artefacts.

### 3. Explainability and audit readiness

Regulators, product owners, and internal auditors increasingly ask *why* a model behaves as it does. KMDS provides a structured answer: the sequence of observations, with rationale and sequence numbers, is captured in a reloadable RDF file. The executive summary CLI can generate a non-technical narrative from that file on demand — reducing the time to produce a compliance artefact from hours to seconds.

### 4. Semantic retrieval bridges the vocabulary gap

A team member looking for "why we dropped the age variable" may not remember the exact phrasing used when the observation was logged. KMDS's semantic vector index (ChromaDB + sentence-transformers, fully open-source) retrieves findings based on meaning rather than exact keyword match, reducing the chance that relevant prior work is overlooked.

---

## Management Headline

> KMDS moves data science project knowledge from **analysts' heads and notebook comments** to a **queryable, shareable, audit-ready record** — without adding friction to the workflow.

---

## Key Differentiators

| Feature | Why It Matters |
|---|---|
| **Ontology-backed observation types** | Findings are classified (exploratory / data rep / model choice / model selection), not free-text blobs — enabling phase-specific querying |
| **Natural language ingestion** | Any team member can log or query without learning the schema; LLM classifies the observation type automatically |
| **LLM search orchestrator with Pydantic routing** | Routes questions to the right template rather than returning unranked keyword hits; falls back gracefully to semantic search |
| **Executive summary CLI** | Generates a non-technical narrative from the KB — useful for stakeholder reviews and compliance artefacts |
| **Fully open-source runtime** | sentence-transformers, ChromaDB, owlready2 — no proprietary vector DB or embedding API required |
| **CLI-first design** | Every major feature usable from a shell — fits CI pipelines, reproducible scripts, and non-notebook workflows |

---

## Typical Workflow Impact

### Before KMDS (medium-sized project, 2 analysts)

| Step | Who | Estimated time |
|---|---|---|
| Log findings during EDA | Analyst | Ad-hoc, often deferred or skipped |
| Find a prior observation during model phase | Analyst | 20–40 min (searching notebooks, Slack, memory) |
| Prepare exec summary before stakeholder review | Senior analyst | 2–4 hours |
| Onboard a replacement analyst | Both | 1–2 days of context transfer |
| Answer an audit question about a modelling choice | Senior analyst | 30–60 min (reconstruction from code) |

### After KMDS

| Step | Who | Estimated time |
|---|---|---|
| Log a finding | Any team member | 1–2 min via CLI or Python API |
| Find a prior observation | Any team member | < 1 min (`kmds-ask` or `kmds-search`) |
| Prepare exec summary | Anyone | < 30 seconds (`kmds-exec-summary`) |
| Onboard a new analyst | New analyst (self-serve) | 15–30 min reading KB summary + asking questions |
| Answer an audit question | Anyone | < 5 min (KB query + summary export) |

The most significant reduction is in the **onboarding and audit scenarios** — which are high-cost, high-stress, and currently have no systematic support in most teams.

---

## Risk Reduction

- **Knowledge single-point-of-failure:** Without KMDS, project context lives with the analyst who built it. KMDS externalises it into a versioned, shareable file.
- **Model drift without audit trail:** Teams that cannot explain a model's design choices are exposed when a model degrades or is challenged. KMDS provides a timestamped sequence of decisions.
- **Rework from forgotten context:** Analysts re-explore data or re-test models already evaluated. KMDS semantic search surfaces prior work before rework begins.
- **LLM routing errors:** The search orchestrator constrains LLM output with a Pydantic schema and falls back to vector search if the LLM is uncertain — so users receive useful answers even when the LLM misfires.
- **Vendor lock-in:** All runtime components (ChromaDB, sentence-transformers, owlready2) are Apache/MIT-licensed open-source libraries. The knowledge base is stored as standard RDF/OWL XML.

---

## Technical Confidence

- ✅ Ontology-backed observation capture tested across analytics and ML example workflows
- ✅ Semantic index build and search validated (ChromaDB ephemeral and persistent)
- ✅ LLM search orchestrator tested with Google GenAI and local callable fallback
- ✅ Natural language ingestion validated across all five intent/observation types
- ✅ Executive summary CLI tested in text and markdown output modes
- ✅ Summary-log CLI tested for both create and update project modes
- ✅ All CLI entry points covered by unit and integration tests in `tests/`
- ✅ Package installable via `pip install kmds`; documented on ReadTheDocs
- ✅ Two worked examples (analytics and ML) shipped as package resources with notebooks
