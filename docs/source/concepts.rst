Concepts
#########
This section contains the description of concepts used in documenting analytics and machine learning use cases with KMDS.

Who Is KMDS For?
****************
KMDS was originally designed for data scientists working in Python notebooks. Recent additions to the CLI toolset and the natural-language ingestion feature mean it is now practical for a broader set of users.

- **Data scientists** have access to the full Python API, notebook examples, semantic search, and the LLM-based search orchestrator.
- **Software developers** can automate knowledge capture in pipelines using CLI commands and the Python API.
- **Business analysts** who know Python can use the CLI tools and the natural-language ingestion feature to log findings without writing ontology code.

The Knowledge Management Workflow Context
*******************************************
In a typical enterprise setting, we have business or organizational applications that customers and employees interact with. These interactions generate business operational data that is subsequently cleaned and transformed for various analytical or machine-learning projects. A schematic of this process is available in `the repository <https://github.com/rajivsam/KMDS/blob/main/feature_documentation/knowledge_management_in_DS.md>`_ . The operational data is usually transformed to the needs of each analytic or machine learning use case. This transformed representation is the *data representation* for the specific use case. Data representations are developed by knowledge workers, such as business analysts, and technical staff members such as data engineers and data scientists. The correct data representation for a particular use case can evolve over time because there is a *discovery* aspect to data analysis and data science work. Baselining representations and documenting the rationale for the changes and evolution of *data representations* is important to facilitate quick implementation iterations. This is what KMDS can help with.


Workflows
*********
A workflow is a sequence of processing tasks to develop a product for your use case. A product can be a report, a model, a set of features or other data products that you can think of. Typically, in a data science setting, we are interested in developing either an *analytics workflow* or a *machine learning* workflow. Typically in an analytics workflow, the data set is fixed, there is a specific set of exploration questions and the computational approach to get the answers to these questions is established. In contrast, a machine learning workflow may need principled experimentation to accomplish a goal. See `this video <https://www.youtube.com/watch?v=dcXqhMqhZUo>`_ from IBM for more details. In each workflow, the tasks performed can be categorized as either *exploratory*, *data representation*, or, *modeling* based on the nature of the processing performed by the task. See `the workflow typs page in the repository <https://github.com/rajivsam/KMDS/blob/main/feature_documentation/km_app_pipeline.md>`_ for more information.

Observation Logging
*******************
The following are guidelines for what must be captured as part of documenting a workflow.


1. In general, all decisions that change input data or data representations need to be logged with documentation that makes it possible to reproduce these changes. In other words, data scientists can reproduce the intermediate data artifacts from the input data by following the logged documentation.

2. The rationale for making modeling choices and the experimental pipelines that informed the rationale should be logged with documentation.

3. The methodology to evaluate task performance must be logged.


4. Assumptions for modeling must be logged.

Searching and Retrieving Knowledge
***********************************

Once observations are logged to a KMDS knowledge base, KMDS provides two ways
to retrieve them.

**Semantic search** builds a vector index from the text of all logged
observations and returns the most relevant findings for a natural-language
query. Results include a similarity distance so you can assess relevance. This
works without an external API key.

.. code:: python

   from kmds.search import SemanticIndex

   idx = SemanticIndex()
   idx.build("./my_project.xml")
   results = idx.search("What data quality problems were found?", n_results=5)
   for r in results:
       print(r["obs_type"], "|", r["finding"])

**The LLM search orchestrator** adds an intent-routing layer on top of the
vector index. It classifies a free-form question into one of the available
observation-query templates, extracts structured filter parameters, executes the
best template, and synthesises the raw results into a concise plain-English
answer. When no template matches, it falls back to semantic search automatically.

Both capabilities are also available from the command line as ``kmds-search``
and ``kmds-ask``. See the :doc:`search_orchestrator` page for a complete guide
and template reference.

Natural Language Observation Ingestion
***************************************

Logging observations traditionally requires writing Python code against the KMDS ontology classes. KMDS also supports a natural-language ingestion path that lowers this barrier.

Given a free-form statement such as *"Ticket creation and closed timestamps have inconsistent datetime formats"*, the ingestion feature:

1. Classifies the text into the correct KMDS observation family and type.
2. Extracts structured entities such as the affected component, a numeric metric, or a timestamp.
3. Validates that the input is specific enough to form a meaningful observation.
4. Either returns a structured summary or logs the observation directly to a knowledge base.

Two interaction modes are available:

- **Summary mode** — classify and describe without modifying any file.
- **Log mode** — validate, create the RDF observation, and save it to a KMDS project file.

All modes are accessible from the Python API, from a notebook cell, and from the ``kmds-observe`` CLI command. See the :doc:`natural_language_ingestion` page for complete examples.

Glossary of Observation Types
******************************

The tasks within a workflow can be categorized as *exploratory*, *data representation* or *modeling* depending on the nature of the task performed. A description of these types and guidelines for logging observations belonging to these types are provided in `the observation glossary <https://github.com/rajivsam/KMDS/blob/main/feature_documentation/glossary_observation_types.md>`_.

Knowledge Graphs
*****************
The developed documentation is stored as an *RDF* graph. This graph can be shared between workflows. In other words, the following scenarios are possible:

1. You could start with an exploratory workflow, save it, and load the exploratory workflow in a notebook where you are evaluating different data representations for a use case, once you have determined a suitable data representation you can update the workflow with your observations from data representation experimentation and save the workflow. You can then load the workflow with observations from exploratory data analysis and data representations in a notebook where you are performing modeling experiments. Once you have determined a suitable model for your use case, you can update the workflow with your observations from modeling. After completing the modeling phase to your satisfaction, you can save the workflow with the documentation to a network location and then load it and review your observations.

2. For workflows that require extensive experimentation, you can create separate workflows for experimentation and then indicate that your use case workflow depends on these experiments. 

Examples of both these scenarios are provided. The repository contains a page explaining the implementation steps for managing the life cycle of the `knowledge graph <https://github.com/rajivsam/KMDS/blob/main/feature_documentation/ontology_management.md>`_ . Please see the `ontology <https://github.com/rajivsam/KMDS/blob/main/kmds/ontology/kmds_ontology.py>`_ for details of the knowledge graph.







   