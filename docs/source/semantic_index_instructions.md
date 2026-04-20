# Semantic Index

The semantic index feature embeds all observation findings from a KMDS RDF knowledge base into a vector database, enabling natural language search over captured knowledge.

## Technology

| Component | Library | Version |
|-----------|---------|---------|
| Embeddings | [sentence-transformers](https://www.sbert.net/) (`all-MiniLM-L6-v2`) | ≥ 3.0 |
| Vector store | [ChromaDB](https://www.trychroma.com/) | ≥ 0.6 |

Both libraries are open source with large community footprints and active maintenance.

## What gets indexed

Every text-bearing node in the knowledge graph is indexed:

- **Workflow description** — the top-level `description` property of the workflow
- **Exploratory observations** — EDA findings (`has_exploratory_observations`)
- **Data representation observations** — feature engineering findings
- **Modelling choice observations** — modelling decisions and assumptions
- **Model selection observations** — model selection results and summaries

Each indexed document stores the following metadata alongside the text:

| Field | Description |
|-------|-------------|
| `obs_type` | Observation category (e.g. `"Data Quality Observation"`) |
| `workflow_name` | Name of the parent workflow |
| `finding_seq` | Original sequence number of the finding |
| `intent` | Intent tag when present on the observation |

## Python API

### Build an in-memory index and search

```python
from kmds.search import SemanticIndex

idx = SemanticIndex()               # ephemeral (in-memory only)
idx.build("path/to/kb.xml")        # index all observations

results = idx.search("missing values in intake data", n_results=5)

for r in results:
    print(r["obs_type"], "|", r["finding"])
    print("  distance:", r["distance"])   # cosine distance, lower = more similar
```

### Persist the index to disk

Pass `persist_dir` to save the index between sessions. Subsequent calls with the same directory skip rebuilding if the index is already populated.

```python
from kmds.search import SemanticIndex

# First run — build and save
idx = SemanticIndex(persist_dir="./kb_index")
idx.build("path/to/kb.xml")

# Later runs — load and query without rebuilding
idx = SemanticIndex(persist_dir="./kb_index")
results = idx.search("imputation strategy")
```

### Build from an already-loaded ontology

```python
from kmds.search import SemanticIndex
from kmds.utils.load_utils import load_kb

onto = load_kb("path/to/kb.xml")

idx = SemanticIndex()
idx.build_from_onto(onto)

results = idx.search("model accuracy on test set")
```

### Use a different embedding model

Any model from the [sentence-transformers model hub](https://huggingface.co/sentence-transformers) can be used:

```python
idx = SemanticIndex(model_name="all-mpnet-base-v2")
idx.build("path/to/kb.xml")
```

### Search result structure

`search()` returns a list of dicts, one per result, ordered by ascending cosine distance (most similar first):

```python
[
    {
        "finding":       "Missing category labels found in intake data",
        "obs_type":      "Data Quality Observation",
        "workflow_name": "retail_analytics_workflow",
        "finding_seq":   1,
        "distance":      0.1234,
        "intent":        "DATA_UNDERSTANDING"   # only present when set
    },
    ...
]
```

### Utility methods

```python
idx.count()   # number of documents currently in the index
idx.clear()   # remove all documents from the index
```

## CLI

```
kmds-search --project-file <KB_FILE> --query <QUERY> [options]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--project-file` | *(required)* | Path to the KMDS knowledge-base XML file |
| `--query` | *(required)* | Natural language search query |
| `--n-results` | `5` | Maximum number of results to return |
| `--persist-dir` | *(none)* | Directory to persist/load the index; omit for in-memory only |
| `--model` | `all-MiniLM-L6-v2` | Sentence-transformers model name |
| `--output-format` | `text` | `text` or `json` |

### Examples

```bash
# Basic search
kmds-search --project-file kb.xml --query "missing values in intake data"

# Limit results
kmds-search --project-file kb.xml --query "imputation" --n-results 3

# Persist index for fast repeated queries
kmds-search --project-file kb.xml --query "model accuracy" --persist-dir ./idx

# JSON output (useful for piping to other tools)
kmds-search --project-file kb.xml --query "feature engineering" --output-format json
```
