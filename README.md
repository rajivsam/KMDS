<p align="center">
  <a href="https://kmds.readthedocs.io/en/latest/">
    <img width="460" height="300" src="https://raw.githubusercontent.com/rajivsam/KMDS/main/images/kmds_logo_resized.jpg" alt="KMDS Logo">
  </a>
</p>

<h1 align="center">Knowledge Management for Data Science (KMDS)</h1>

<p align="center">
  <strong>Capture, organize, and reuse knowledge from your data science experiments.</strong>
</p>

<p align="center">
  <a href="https://zenodo.org/doi/10.5281/zenodo.10695270"><img src="https://zenodo.org/badge/753950832.svg" alt="DOI"></a>
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License"></a>
  <a href="https://kmds.readthedocs.io/en/latest/?badge=latest"><img src="https://readthedocs.org/projects/kmds/badge/?version=latest" alt="Documentation Status"></a>
</p>

---

## 🌟 What is KMDS?

KMDS is a Python-based tool for systematic knowledge management in data science and analytics projects. It helps you document the incremental process of exploration, data preparation, and model development — capturing context, decisions, and rationale so that valuable insights are not lost over time.

### The Problem It Solves

Experimental work generates a stream of decisions and findings. The context and rationale behind each step are often documented ad-hoc, if at all. When it is time to revisit a question or build on earlier work, the research trail has gone cold. KMDS fixes this by providing a structured, ontology-backed way to log, search, and share your findings.

### Who Can Use KMDS?

KMDS was originally designed for data scientists writing Python. Recent additions to the CLI and natural-language tooling mean it is now practical for a broader set of users:

| User | How they interact with KMDS |
|---|---|
| **Data scientist** | Python API, notebooks, CLI — full access to all features |
| **Software developer** | CLI tools and Python API for automating knowledge capture in pipelines |
| **Business analyst** | CLI commands and natural-language ingestion — no ontology code required |

🎥 **Watch a quick overview of KMDS:** [YouTube Video](https://www.youtube.com/watch?v=n7gE6bfLWtI)

---

## ✨ Key Features

- **Structured Observation Capture:** Log findings from exploration, data representation, modeling choice, and model selection stages using Python or the CLI.
- **Natural Language Ingestion:** Describe a finding in plain English — KMDS classifies it, extracts structured entities, and optionally logs it to the knowledge base. No ontology code required.
- **Ontology-Backed Knowledge Base:** Store and reload workflow knowledge as RDF/OWL artifacts that can be shared across projects and teams.
- **Semantic Search:** Build a vector index from your knowledge base and retrieve relevant findings with natural-language queries.
- **LLM Search Orchestrator:** Route natural-language questions to structured KMDS search templates with automatic semantic fallback.
- **CLI-First Usability:** Every major feature is accessible as a command-line tool — usable by developers and analysts without writing notebook code.
- **Simple Reporting Surface:** Load observations into tabular form for review, sharing, and downstream analysis.

---

## 🚀 Getting Started

### 1. Installation

Install KMDS in your Python environment:

```bash
pip install kmds
```

### 2. Usage

As you work through your analysis, log your findings to `kmds`. Check out the examples below.

### 3. Quick Summary Logging (CLI)

KMDS now supports logging exploratory observations directly from a free-text project summary. This is useful for business analysts and other non-developers who want to capture findings quickly.

Application workflow example (explicit, non-interactive):

```bash
kmds-summary-log \
  --summary "This is a daily reporting workflow for support operations. Missing category labels were found in intake data." \
  --workflow-name "support_reporting_intake" \
  --workflow-type application \
  --project-file ./support_reporting_intake.xml \
  --create-project \
  --no-prompt
```

Ambiguous summary example (interactive prompt):

```bash
kmds-summary-log \
  --summary "Project kickoff notes for the upcoming quarter." \
  --workflow-name "quarterly_kickoff_notes" \
  --project-file ./quarterly_kickoff_notes.xml \
  --create-project
```

In the ambiguous case, KMDS will ask whether the workflow is `application` or `experimental`, then continue logging exploratory observations.

### 4. Export Executive Summary (CLI)

You can export a non-technical executive summary from a KMDS project file.

```bash
kmds-exec-summary \
  --project-file ./support_reporting_intake.xml \
  --output-file ./support_reporting_exec_summary.txt
```

Optional LLM mode (falls back to local summary if API/model is unavailable):

```bash
kmds-exec-summary \
  --project-file ./support_reporting_intake.xml \
  --output-file ./support_reporting_exec_summary.txt \
  --use-llm \
  --model gemini-1.5-flash
```

Markdown output option:

```bash
kmds-exec-summary \
  --project-file ./support_reporting_intake.xml \
  --output-file ./support_reporting_exec_summary.md \
  --format markdown
```

### 5. Natural Language Observation Ingestion

KMDS can classify a free-form natural language statement into the existing KMDS observation schema, extract structured entities, and either return a summary or log the result into a KMDS knowledge base.

Summary mode example:

```bash
kmds-observe \
  --text "The model accuracy dropped by 5% after pruning on 2026-04-20." \
  --mode summary \
  --output-format json
```

Log mode example for a new project:

```bash
kmds-observe \
  --text "Missing values were observed in the customer_age field during intake validation." \
  --mode log \
  --workflow-name "support_reporting_intake" \
  --project-file ./support_reporting_intake.xml \
  --workflow-type application \
  --create-project
```

Python API example:

```python
from kmds.utils.natural_language_observation import map_text_to_observation

mapping = map_text_to_observation(
    "We engineered a rolling 7 day demand feature from timestamped order counts."
)

print(mapping.workflow_family)
print(mapping.observation_type)
print(mapping.extracted_entities)
```

### 6. Semantic Search (CLI)

Build a vector index from a KMDS knowledge base and retrieve relevant findings with a natural-language query. No API key required.

```bash
kmds-search \
  --kb ./support_reporting_intake.xml \
  --query "What data quality issues were found?" \
  --n-results 5
```

Or from the Python API:

```python
from kmds.search import SemanticIndex

idx = SemanticIndex()
idx.build("./support_reporting_intake.xml")
results = idx.search("What data quality issues were found?", n_results=5)
for r in results:
    print(r["obs_type"], "|", r["finding"])
```

### 7. LLM Search Orchestrator (CLI)

Ask a free-form question. The orchestrator routes it to the best KMDS observation-query template using an LLM, executes the template, and synthesises a plain-English answer. Falls back to semantic search automatically.

```bash
export GOOGLE_API_KEY="your-api-key"
kmds-ask \
  --kb ./support_reporting_intake.xml \
  --query "What assumptions drove the final model selection?"
```

The full documentation covers custom LLM functions, available routing templates, and output formats.



This repository includes two detailed examples:

-   **Analytics Example:** Evaluates the effectiveness of a ticket resolution help desk.
    -   [Notebooks](examples_of_use/analytics)
    -   [Video Summary](https://www.youtube.com/watch?v=zmm0O4_fK_c)
    -   [Infographic](examples_of_use/analytics/usecase_overview_mindmap.png)

-   **Machine Learning Example:** Uses Principal Component Analysis (PCA) to summarize online store sales activity.
    -   [Notebooks](examples_of_use/machine_learning)
    -   [Infographic](examples_of_use/machine_learning/ml_infographic_kmds.png)

---

## 🤝 Contributing

We welcome contributions! If you have an idea for a new feature or would like to report a bug, please open an issue. If you'd like to contribute code, please fork the repository and submit a pull request.

---

## 📄 License

This project is licensed under the Apache 2.0 License. See the [LICENSE](https://www.apache.org/licenses/LICENSE-2.0.txt) file for details.

---

## 📞 Contact

If you have questions or are interested in the following, please [schedule a meeting](https://calendly.com/rajiv-sambasivan/help-with-kmds-feature):

-   Help with a data analysis task for your use case.
-   Developing a custom ontology-based solution.
-   Integrating KMDS with other tools in your data science stack.