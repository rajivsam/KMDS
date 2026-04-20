
Build and Installation
***********************
The package can be installed from PyPi as follows

.. code:: bash

    pip install kmds

A conda version of the package is not available at the moment.


Please see the `the build instructions page <https://github.com/rajivsam/KMDS/blob/main/build_instructions/build_instructions.md>`_ for details of building the project and maintaining documentation.


Quick Summary Logging (CLI)
***************************

You can create exploratory observations directly from a project summary block.

Application workflow example (explicit and non-interactive):

.. code:: bash

        kmds-summary-log \
            --summary "This is a daily reporting workflow for support operations. Missing category labels were found in intake data." \
            --workflow-name "support_reporting_intake" \
            --workflow-type application \
            --project-file ./support_reporting_intake.xml \
            --create-project \
            --no-prompt

Ambiguous summary example (interactive prompt):

.. code:: bash

        kmds-summary-log \
            --summary "Project kickoff notes for the upcoming quarter." \
            --workflow-name "quarterly_kickoff_notes" \
            --project-file ./quarterly_kickoff_notes.xml \
            --create-project

In the ambiguous case, KMDS prompts for workflow type and then logs exploratory observations.


Natural Language Observation Ingestion
**************************************

KMDS can also ingest a single free-form natural language observation and map it
to the existing ontology schema.

Summary mode example:

.. code:: bash

        kmds-observe \
            --text "The model accuracy dropped by 5% after pruning on 2026-04-20." \
            --mode summary \
            --output-format json

Log mode example:

.. code:: bash

        kmds-observe \
            --text "Missing values were observed in the customer_age field during intake validation." \
            --mode log \
            --workflow-name "support_reporting_intake" \
            --project-file ./support_reporting_intake.xml \
            --workflow-type application \
            --create-project

For complete examples of all interaction modes, see the
``Natural Language Ingestion`` documentation page.


Semantic Search (CLI)
*********************

Build a vector index from a KMDS knowledge base and search it with a
natural-language query.

.. code:: bash

        kmds-search \
            --kb ./support_reporting_intake.xml \
            --query "What data quality issues were found?" \
            --n-results 5

JSON output:

.. code:: bash

        kmds-search \
            --kb ./support_reporting_intake.xml \
            --query "What data quality issues were found?" \
            --output-format json


LLM Search Orchestrator (CLI)
*****************************

Ask a free-form question; the orchestrator routes it to the best KMDS search
template using an LLM and synthesises a plain-English answer. Falls back to
semantic search automatically when routing is uncertain.

.. code:: bash

        export GOOGLE_API_KEY="your-api-key"
        kmds-ask \
            --kb ./support_reporting_intake.xml \
            --query "What assumptions drove the final model selection?"

JSON output:

.. code:: bash

        kmds-ask \
            --kb ./support_reporting_intake.xml \
            --query "What assumptions drove the final model selection?" \
            --output-format json

See the ``Natural Language Search`` documentation page for a full guide,
including how to supply a custom LLM function.

