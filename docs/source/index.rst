.. KMDS documentation master file, created by
   sphinx-quickstart on Mon Feb 26 10:22:56 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Knowledge Management for Data Science
======================================
KMDS, Knowledge Management for Data Science, is a Python library to document, search, and retrieve knowledge from your analytics and machine learning workflows. The knowledge captured as part of your development process is stored as a *RDF* graph. These graphs can be shared between projects, or updated sequentially by different iterations of the same project.

KMDS provides five integrated capabilities:

1. **Structured observation capture** — log findings from exploration, data representation, modelling choice, and model selection phases using the Python API or CLI.
2. **Natural language ingestion** — describe a finding in plain English; KMDS classifies it, extracts structured entities, and either returns a structured summary or logs it directly to a knowledge base.
3. **Semantic search** — build a vector index from a knowledge base and retrieve relevant observations using natural-language queries.
4. **LLM search orchestration** — ask free-form questions; an LLM routes the question to the best observation-query template and synthesises a plain-English answer, with automatic semantic fallback.
5. **Reporting** — load observations into tabular form for review, sharing, and downstream analysis.

The documentation is organised into concepts, recipes, and feature-specific pages. The concepts section describes the ideas that underpin knowledge capture. The recipes section illustrates those concepts with real-world analytics and machine-learning examples.


.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   Installation <install>
   Concepts <concepts>
   Natural Language Ingestion <natural_language_ingestion>
   Natural Language Search <search_orchestrator>
   Modules <modules>


KMDS 
=====
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

