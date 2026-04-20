Natural Language Search with the Search Orchestrator
######################################################

The KMDS *Search Orchestrator* lets you ask free-form questions about a project
knowledge base and receive a plain-English answer.  Under the hood it uses an
LLM as a **router** to classify your intent, execute the best matching
observation-query template, and synthesise the raw results into a readable
response.  When no structured template matches, it falls back automatically to
semantic vector search.

.. contents:: Steps
   :local:
   :depth: 1

----

Overview
========

The orchestrator follows five logical steps every time you call it:

.. list-table::
   :widths: 10 25 65
   :header-rows: 1

   * - Step
     - Label
     - What happens
   * - 1
     - **Context Injection**
     - A *tool description* — a catalogue of all available search templates and
       their purpose — is injected into the LLM prompt so the model always knows
       its options.
   * - 2
     - **Intent Classification & Entity Extraction**
     - The LLM analyses your query and returns a Pydantic-validated JSON payload
       identifying which template to invoke and any filter parameters
       (observation type, keyword, sequence range) it extracted.
   * - 3
     - **Template Execution**
     - The matching KMDS API function is called against the loaded knowledge base
       with the extracted filters applied.
   * - 4
     - **LLM Synthesis**
     - The LLM converts the raw observation records into a concise natural
       language answer.
   * - 5
     - **Semantic Fallback** *(catch-all)*
     - If no template matches, or if a template returns zero results, the
       ChromaDB semantic vector index is queried instead.

.. note::

   **Why not LlamaIndex (for now)?**
   KMDS currently uses a custom orchestrator because it provides strict control
   over template routing, filter validation, and fallback behaviour with a
   smaller runtime dependency surface. This keeps behaviour predictable for
   ontology-specific queries and simplifies maintenance. We may revisit
   LlamaIndex later if we need broader multi-retriever orchestration,
   connector breadth, or rapid RAG pipeline experimentation.

Available Search Templates
==========================

+-----------------------------------+--------------------------------------------------+
| Template                          | Best for                                         |
+===================================+==================================================+
| ``exploratory_search``            | Data quality, missing values, outliers,          |
|                                   | distributions, initial data understanding        |
+-----------------------------------+--------------------------------------------------+
| ``data_representation_search``    | Feature engineering, transformations, encodings, |
|                                   | scaling, data preparation decisions              |
+-----------------------------------+--------------------------------------------------+
| ``modelling_choice_search``       | Algorithm selection rationale, modelling         |
|                                   | assumptions, hyperparameter decisions            |
+-----------------------------------+--------------------------------------------------+
| ``model_selection_search``        | Model comparison, evaluation metrics,            |
|                                   | benchmarking, final model recommendation         |
+-----------------------------------+--------------------------------------------------+
| ``all_observations_search``       | Broad cross-phase questions                      |
+-----------------------------------+--------------------------------------------------+
| ``semantic_search`` *(fallback)*  | Nuanced natural-language similarity queries      |
+-----------------------------------+--------------------------------------------------+

----

Step-by-Step Usage
==================

Step A – Prerequisites
-----------------------

Install the package with all dependencies::

    pip install kmds          # core (pydantic, chromadb, sentence-transformers included)

For LLM-powered routing and synthesis you need a Google GenAI API key
(``gemini-1.5-flash`` is used by default)::

    export GOOGLE_API_KEY="your-google-api-key"

.. note::

   If you prefer a different LLM (OpenAI, Anthropic, local Ollama, etc.),
   pass a ``llm_fn`` callable — see :ref:`custom-llm` below.

Step B – Build or Load a Knowledge Base
----------------------------------------

You need a ``.xml`` knowledge-base file produced by a KMDS workflow.  A test
knowledge base ships with the package::

    from importlib.resources import files
    kb_path = str(files("kmds.examples").joinpath("example_analytics_kb_app_workflow.xml"))

Or use your own project file::

    kb_path = "path/to/my_project_kb.xml"

Step C – Initialise the Orchestrator
--------------------------------------

.. code-block:: python

    from kmds.search import SearchOrchestrator

    orc = SearchOrchestrator(
        kb_path=kb_path,
        persist_dir="./my_index",   # omit for in-memory (rebuilt each session)
    )

What happens here:

* The knowledge base is loaded into memory once.
* The semantic vector index (ChromaDB) is built from all observation findings
  and persisted to ``./my_index`` for fast reload on subsequent runs.

Step D – Ask a Question
------------------------

.. code-block:: python

    result = orc.ask("What data quality issues were found during exploration?")

    print(result.answer)          # synthesised natural language answer
    print(result.intent_class)    # which template was used
    print(result.route_explanation)
    print(result.results)         # raw observation records

The returned :class:`~kmds.search.search_orchestrator.OrchestratorResult`
always has these attributes:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Attribute
     - Description
   * - ``answer``
     - Synthesised natural language answer (string).
   * - ``intent_class``
     - The template that was ultimately executed.
   * - ``route_explanation``
     - The LLM's one-sentence reason for choosing that template.
   * - ``results``
     - List of raw observation dicts (``obs_type``, ``finding``,
       ``finding_seq``, optional ``intent``, optional ``distance``).

Step E – Inspect Raw Results
-----------------------------

.. code-block:: python

    for r in result.results:
        print(r["obs_type"], "|", r["finding"])

Step F – Use the CLI
---------------------

The orchestrator is also available as a command-line tool::

    # Basic usage
    kmds-ask --project-file my_project.xml \
              --query "What feature engineering steps were taken?"

    # Persist the index for fast repeated queries
    kmds-ask --project-file my_project.xml \
              --query "Which model was selected and why?" \
              --persist-dir ./my_idx

    # Show routing decision and raw records
    kmds-ask --project-file my_project.xml \
              --query "transformation decisions" \
              --verbose

    # Machine-readable JSON output
    kmds-ask --project-file my_project.xml \
              --query "model evaluation metrics" \
              --output-format json

    # Use a different LLM model
    kmds-ask --project-file my_project.xml \
              --query "data quality" \
              --model gemini-2.0-flash

----

.. _custom-llm:

Using a Custom LLM Backend
===========================

Pass any callable that accepts a ``str`` prompt and returns a ``str``
response::

    def my_llm(prompt: str) -> str:
        # Example using OpenAI
        import openai
        client = openai.OpenAI(api_key="sk-...")
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content

    orc = SearchOrchestrator(kb_path=kb_path, llm_fn=my_llm)
    result = orc.ask("What modelling assumptions were made?")
    print(result.answer)

----

Fallback Behaviour
==================

The orchestrator is designed to always return *something*:

1. If the LLM is unreachable → router falls back to semantic vector search.
2. If the JSON response cannot be parsed → falls back to semantic search.
3. If the chosen template returns zero observations → falls back to semantic
   search.
4. If the synthesis LLM call fails → raw records are formatted as plain text.

----

Worked Example
==============

.. code-block:: python

    import os
    from importlib.resources import files
    from kmds.search import SearchOrchestrator

    os.environ["GOOGLE_API_KEY"] = "your-key-here"

    kb_path = str(files("kmds.examples").joinpath("example_ml_kb_exp_workflow.xml"))

    orc = SearchOrchestrator(kb_path=kb_path, persist_dir="./ml_idx")

    questions = [
        "What data quality issues were encountered?",
        "Which features were engineered and why?",
        "What modelling assumptions were made?",
        "Which model was finally selected and what were its evaluation metrics?",
        "Summarise the key findings across all phases.",
    ]

    for q in questions:
        result = orc.ask(q)
        print(f"Q: {q}")
        print(f"   Template used : {result.intent_class}")
        print(f"   Answer        : {result.answer[:200]}")
        print()

----

Pydantic Schema Reference
==========================

The router output is validated against:

.. autoclass:: kmds.search.search_orchestrator.SearchFilters
   :members:

.. autoclass:: kmds.search.search_orchestrator.OrchestratorRoute
   :members:

API Reference
=============

.. autoclass:: kmds.search.search_orchestrator.SearchOrchestrator
   :members: ask, __init__
   :undoc-members:

.. autoclass:: kmds.search.search_orchestrator.OrchestratorResult
   :members:
   :undoc-members:
