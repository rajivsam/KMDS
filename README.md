<p align="center">
  <a href="https://readthedocs.io">
    <img width="460" height="300" src="https://githubusercontent.com" alt="KMDS Logo">
  </a>
</p>

<h1 align="center">Knowledge Management for Data Science (KMDS)</h1>

<p align="center">
  <strong>Capture, organize, and reuse knowledge from your data science experiments.</strong>
</p>

<p align="center">
  <a href="https://zenodo.org"><img src="https://zenodo.org" alt="DOI"></a>
  <a href="https://opensource.org"><img src="https://shields.io" alt="License"></a>
  <a href="https://readthedocs.io?badge=latest"><img src="https://readthedocs.org" alt="Documentation Status"></a>
</p>

---

## 🌟 What is KMDS?

KMDS is an ontology-backed ecosystem for systematic knowledge management in data science and analytics workflows. It documents the incremental process of experimentation, data exploration, and model selection—capturing decisions, rationale, and repository schemas so that valuable insights are never lost over time.

### The Problem It Solves

Experimental work generates a fragmented stream of insights, local documentation, and Jupyter notebooks. This context is typically lost when a research trail goes cold. The KMDS ecosystem fixes this by providing a unified, structured approach to log, map, search, and visually audit your data engineering artifacts.

### Who Can Use KMDS?


| User                   | How they interact with KMDS                                                     |
| :----------------------- | :-------------------------------------------------------------------------------- |
| **Data scientist**     | Python API, local LLM integrations, notebooks, and CLI framework                |
| **Software developer** | Automated repo mapping utilities and pipeline automated logging hooks           |
| **Business analyst**   | Interactive UI Workbench Dashboard and plain-English natural language ingestion |

🎥 **Watch a quick overview of KMDS:** [YouTube Video](https://youtube.com)

---

## ✨ Key Features

- **Interactive UI Workbench (`kmds-ui`):** View, edit, and safely serialize knowledge graphs with special handling for long text notes and file context preservation.
- **Automated Repository Scanning (`kmds-data-helper`):** Parse local codebases using a multi-persona engine (Data Scientist, Tech Lead, Architect) to synthesize documentation and code into structured knowledge graphs.
- **Natural Language Ingestion:** Describe insights in plain English for automatic logging to your ontology graph.
- **Semantic Vector Search:** Build high-performance local vector indices for querying analytical findings.
- **LLM Search Orchestration:** Use Ollama-powered, intelligent routing for complex knowledge queries.

---

## 📂 KMDS Data Helper (`kmds-data-helper`)

The `kmds-data-helper` package introduces a multi-persona analysis framework for existing data science repositories. Using local LLMs (via Ollama), it scans documentation, schemas, and notebooks to output complete KMDS knowledge graphs.

### Key Features

* **Toggleable Role Personas:** Switch between Data Scientist, Tech Lead, and Architect behaviors via a `kmds_config.yaml` file.
* **Automated Artifact Synthesis:** Scans directories to auto-generate structured diagnostic files (`full_service_report.json`, `kmds_summary.json`).
* **Direct Graph Production:** Compiles generated report structures directly into a standardized `project_knowledge_graph.xml`.

---

## 🚀 Getting Started

### 1. Installation

Install the entire modular framework directly from PyPI:

```bash
# Install core logging, UI, and data helper
pip install kmds kmds-ui kmds-data-helper
```

### 2. Using the Interactive UI

Launch your workbench application from the terminal:

```bash
kmds-workbench
```

*Open `http://127.0.0` in your browser.*

### 3. Automatically Building Graphs from Repositories (`kmds-data-helper`)

Set up a project directory containing `documents/`, `notebooks/`, and `data_dictionary/`.

Run the automatic aggregator tool:

```bash
kmds-kb --workspace . --project-file project_knowledge_graph.xml --mode auto
```

To parse individual report paths directly, use the adapter interface command:

```bash
kmds-analyze --input output/full_service_report.json --project-file project_knowledge_graph.xml --create-project --workflow-name kmds_project_workflow --mode auto
```

### 4. Quick Summary Logging via CLI (`kmds`)

```bash
kmds-summary-log \
  --summary "Daily reporting workflow for support operations." \
  --workflow-name "support_reporting" \
  --workflow-type application \
  --project-file ./support_reporting.xml \
  --create-project --no-prompt
```

### 5. Executing Semantic Knowledge Queries

```bash
kmds-search \
  --kb ./project_knowledge_graph.xml \
  --query "What data quality issues were identified?" \
  --n-results 3
```

---

## 🤝 Contributing
