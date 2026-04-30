# KMDS Design History

## Executive Summary

KMDS evolved from a small ontology capture library into a multi-surface knowledge management platform for data science teams. The design history covers six substantive decisions: choosing OWL/RDF as the persistence format, establishing a typed four-phase observation schema, building a semantic vector index over the KB, adding an LLM-driven search orchestrator with schema-constrained routing, introducing natural-language observation ingestion, and designing CLI entry points that make all features accessible without Python or ontology knowledge. Each decision was driven by a clear design question, validated with tests or example notebooks, and kept reversible to protect the small-core architecture.

---

## Iteration Cycle Overview

| Phase | Decision | Key Check | Outcome |
|---|---|---|---|
| 1 | OWL/RDF for knowledge persistence | Can observations be saved, reloaded, and queried without custom serialisation? | ✅ |
| 2 | Typed four-phase observation schema | Does the schema cover the full EDA → modelling lifecycle without over-constraining entries? | ✅ |
| 3 | Semantic index (ChromaDB + sentence-transformers) | Does the index return relevant findings for paraphrased queries? | ✅ |
| 4 | LLM search orchestrator with Pydantic routing | Does constrained routing reduce malformed tool invocations and degrade gracefully? | ✅ |
| 5 | Natural-language observation ingestion | Can free-text input be reliably classified and instantiated without per-type prompt engineering? | ✅ |
| 6 | CLI-first surface for all features | Can a non-Python user log, query, and export summaries from the shell alone? | ✅ |

---

## Phase 1: OWL/RDF as the Knowledge Persistence Format

**Design Question**  
What persistence format should store workflow observations so that they can be reloaded, queried, and shared across sessions and projects without a database server?

**Reasoning**  
Data science projects are not database-backed applications — they live on laptops and shared drives. A flat file format is more practical than standing up a DB. JSON or YAML would work for simple serialisation but offer no semantics: there is no standard way to express that a `ModelSelectionObservation` is a kind of `KMObservation`, or that sequence numbers impose an ordering. OWL/RDF gives the KB a formal type hierarchy and enables SPARQL-style querying via `owlready2`, while still serialising to a single portable `.xml` file.

**Design Check**  
Can a KB created in one process be loaded in a new process, with all observation types and relationships preserved?

**Implementation**

```python
# kmds_ontology.py
onto = get_ontology(get_ontology_path()).load()

with onto:
    class KnowledgeApplicationWorkflow(Workflow): pass
    class ExploratoryObservation(KMObservation): pass
    class ModelSelectionObservation(KMObservation): pass
    ...
    class finding_seq(DataProperty, FunctionalProperty):
        domain = [KMObservation]
        range  = [int]
```

```python
# load_utils.py
def load_kb(kb_path: str) -> Ontology:
    onto = get_ontology(f"file://{kb_path}").load()
    return onto
```

**Validation**  
Example notebooks persist a KB after each workflow phase and reload it to verify that observations survive a round-trip. The `conftest.py` fixture creates a temporary KB and checks that all typed observations are recoverable with `load_observations()`.

---

## Phase 2: Typed Four-Phase Observation Schema

**Design Question**  
How should observations be categorised so that both capture and retrieval can be phase-specific, without forcing analysts to learn ontology internals?

**Reasoning**  
Data science projects follow a recognisable lifecycle: exploratory analysis → data representation → modelling choice → model selection. Collapsing all observations into a single free-text type would lose the ability to ask "what data quality issues were found during EDA?" as a distinct query from "what models were evaluated?". Four typed categories with subtypes (e.g., `ExploratoryTags.DATA_QUALITY_OBSERVATION`, `ModelSelectionTags.COMPARATIVE_PERFORMANCE`) give enough resolution without introducing a new category for every possible finding.

**Design Check**  
Does the schema accommodate real observations from both analytics and ML examples without forcing artificial category assignments?

**Implementation**

```python
# tag_types.py (excerpt)
class ExploratoryTags(str, Enum):
    DATA_QUALITY_OBSERVATION = "DATA_QUALITY_OBSERVATION"
    STATISTICAL_PROPERTY     = "STATISTICAL_PROPERTY"
    ...

class ModelSelectionTags(str, Enum):
    COMPARATIVE_PERFORMANCE  = "COMPARATIVE_PERFORMANCE"
    SELECTION_RATIONALE      = "SELECTION_RATIONALE"
    ...
```

```python
# Logging an observation (Python API)
obs = ExploratoryObservation()
obs.exploratory_observation_type = ExploratoryTags.DATA_QUALITY_OBSERVATION.value
obs.finding = "Missing values in customer_age field: 12% of intake rows"
obs.finding_seq = 1
workflow.has_exploratory_observations.append(obs)
```

**Validation**  
Both the analytics and ML example notebooks use the full four-phase sequence. The `test_knowledge_app_workflow.py` integration test checks that observations from all four phases can be logged and reloaded in the correct sequence.

---

## Phase 3: Semantic Index (ChromaDB + sentence-transformers)

**Design Question**  
How should past observations be made discoverable by analysts who do not remember the exact phrasing used when observations were logged?

**Reasoning**  
Keyword search fails when query vocabulary differs from the stored text — a common situation when findings are logged by one analyst and queried by another weeks later. A vector embedding index over the observation `finding` fields enables semantic retrieval: "problems with age data" retrieves the observation logged as "missing values in customer_age". ChromaDB was chosen because it is Python-native, actively maintained, supports both in-memory (ephemeral) and on-disk (persistent) modes with the same API, and requires no server process. `all-MiniLM-L6-v2` (sentence-transformers) is a well-benchmarked open-source model that runs on CPU in under a second for typical KB sizes.

**Design Check**  
Does the index return the correct observation when a paraphrased query is used, and does a persistent index survive a process restart?

**Implementation**

```python
# semantic_index.py
class SemanticIndex:
    DEFAULT_MODEL = "all-MiniLM-L6-v2"

    def __init__(self, persist_dir=None, model_name=DEFAULT_MODEL):
        self._ef = SentenceTransformerEmbeddingFunction(model_name=model_name)
        if persist_dir:
            self._client = chromadb.PersistentClient(path=persist_dir)
        else:
            self._client = chromadb.EphemeralClient()
        self._collection = self._client.get_or_create_collection(
            name=_COLLECTION_NAME, embedding_function=self._ef
        )

    def build(self, kb_path: str) -> int:
        observations = load_observations(load_kb(kb_path))
        docs = [o["finding"] for o in observations]
        self._collection.add(documents=docs, ids=[str(uuid.uuid4()) for _ in docs],
                             metadatas=observations)
        return len(docs)

    def search(self, query: str, n_results=5):
        return self._collection.query(query_texts=[query], n_results=n_results)
```

**Validation**  
`test_semantic_index.py` builds an index from a fixture KB and verifies that a paraphrased query returns the expected observation. The CLI (`kmds-search`) was validated manually against the analytics example KB.

---

## Phase 4: LLM Search Orchestrator with Pydantic Routing

**Design Question**  
How should free-form natural language questions be routed to phase-specific search templates, and how should the system behave when the LLM cannot confidently classify the intent?

**Reasoning**  
Semantic search retrieves relevant documents but cannot answer structured questions like "what model was selected and why?". A router that maps questions to typed templates can use the KB's phase structure to return more precise answers. The risk is that an LLM returning free-form JSON will occasionally produce invalid arguments, causing silent failures. Using Pydantic to validate the routing payload eliminates this class of error at the boundary. Tool descriptions are injected into the routing prompt so the LLM always knows which templates exist — avoiding hallucinated template names. Semantic search is the fallback when routing confidence is low, so users always receive *something* useful.

**Design Check**  
Does the Pydantic schema catch invalid LLM routing outputs before they reach template execution, and does the semantic fallback activate correctly when no template matches?

**Implementation**

```python
# search_orchestrator.py
class OrchestratorRoute(BaseModel):
    intent_class: IntentClass  # Literal over known template names
    filters: SearchFilters
    explanation: str

def _route(query: str, llm_fn, tool_desc: str) -> OrchestratorRoute:
    prompt = _ROUTING_PROMPT.format(tool_description=tool_desc, query=query)
    raw = llm_fn(prompt)
    try:
        return OrchestratorRoute.model_validate(json.loads(raw))
    except (ValidationError, json.JSONDecodeError):
        # fallback: route to semantic search
        return OrchestratorRoute(intent_class="semantic_search",
                                 filters=SearchFilters(), explanation="routing failed")
```

**Validation**  
`test_search_orchestrator.py` injects a mock LLM that returns both valid and deliberately malformed payloads, confirming that validation errors trigger the semantic fallback rather than raising exceptions.

---

## Phase 5: Natural Language Observation Ingestion

**Design Question**  
Can free-text input be automatically classified into the existing observation schema and instantiated as a valid KB entry, without requiring the analyst to know the observation types?

**Reasoning**  
Lowering the barrier to logging is as important as lowering the barrier to searching. If analysts must look up the right `ExploratoryTags` enum value every time, adoption will be low. The ingestion module uses an LLM to classify intent and extract entities, then maps the result to the correct ontology class and subtype using a validated `FAMILY_METADATA` table. Critically, the module does not generate arbitrary ontology structure — it constrains the LLM output to a `NLObservationMapping` Pydantic model that the rest of the KMDS pipeline can accept directly. The `SUBTYPE_RULES` keyword-matching layer provides a lightweight heuristic fallback that does not depend on an LLM being available.

**Design Check**  
Does the mapping pipeline produce valid, reloadable KB entries for all five observation families, and does it reject ambiguous input with a clear validation error rather than logging garbage?

**Implementation**

```python
# natural_language_observation.py
class NLObservationMapping(BaseModel):
    workflow_family: ObservationFamily
    observation_type: str
    extracted_entities: dict[str, Any]
    finding_sequence: Optional[int]

def map_text_to_observation(text: str, ...) -> NLObservationMapping:
    # 1. LLM classifies family and extracts entities
    # 2. Pydantic validates the output
    # 3. SUBTYPE_RULES refine the subtype if LLM is vague
    ...

def log_text_as_observation(text, workflow_name, project_file_path, ...) -> LogResult:
    mapping = map_text_to_observation(text)
    # instantiate the correct OWL class and attach to workflow
    ...
```

**Validation**  
`test_natural_language_observation.py` tests the mapping pipeline across all five observation families using representative input strings. `test_natural_language_observation_cli.py` validates the `kmds-observe` CLI entry point in both summary and log modes.

---

## Phase 6: CLI-First Surface Design

**Design Question**  
How should the features be surfaced so that users who do not write Python notebooks — business analysts, developers running pipelines — can access the full feature set?

**Reasoning**  
A Python-only API would limit adoption to data scientists. The design goal was that every major feature should be usable from a shell with no notebook required. Each capability was exposed as a separate CLI entry point (`kmds-observe`, `kmds-search`, `kmds-ask`, `kmds-exec-summary`, `kmds-summary-log`) registered in `pyproject.toml`. Each CLI uses `argparse` with explicit `--help` and validates inputs before touching the KB, so errors are reported in plain English rather than Python tracebacks. Interactive prompting (for ambiguous workflow type) is isolated in a `prompt_fn` callback that tests can replace with a deterministic stub.

**Design Check**  
Can each CLI entry point be called with the minimum required arguments and produce correct output without a running Python session?

**Implementation**

```toml
# pyproject.toml
[project.scripts]
kmds-observe       = "kmds.cli.natural_language_observation:main"
kmds-search        = "kmds.cli.semantic_search:main"
kmds-ask           = "kmds.cli.search_orchestrator:main"
kmds-exec-summary  = "kmds.cli.executive_summary:main"
kmds-summary-log   = "kmds.cli.summary_ingest:main"
```

```python
# pattern shared across all CLI modules
def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    # validate, execute, print result
    return 0
```

**Validation**  
Each CLI entry point has a dedicated test file (`test_executive_summary_cli.py`, `test_natural_language_observation_cli.py`, `test_summary_cli.py`). Tests invoke `main(argv=[...])` directly to avoid subprocess overhead while still exercising the full argument-parsing and validation path.
