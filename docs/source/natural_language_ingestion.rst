Natural Language Observation Ingestion
######################################

KMDS can convert a free-form natural language statement into a structured
observation that matches the existing ontology-backed schema.

This feature supports two primary interaction modes:

1. Summary mode: classify the input text, extract entities, and return a
   structured summary without modifying a knowledge base.
2. Log mode: validate the input text, create the matching KMDS observation,
   and save it into a KMDS knowledge base.

The implementation uses open-source tooling only. Classification and entity
extraction are handled by the KMDS parser with spaCy tokenization support when
available.

What The Feature Produces
==========================

Given an input such as:

.. code:: text

   The model accuracy dropped by 5% after pruning on 2026-04-20.

KMDS can produce:

1. A classified observation family and KMDS observation type
2. Extracted entities such as metric, value, timestamp, and affected component
3. A Python snippet that logs the observation into the ontology
4. A JSON-LD payload using the existing KMDS RDF classes and properties
5. A validated logged observation saved into a KMDS knowledge-base file

Supported Observation Families
===============================

The mapper stays within the current KMDS schema and classifies into these
families:

1. Exploratory observations
2. Data representation observations
3. Modelling choice observations
4. Model selection observations
5. Experimental observations

The default workflow phase ordering follows the documented KMDS workflow:

1. Exploratory
2. Data representation
3. Modelling choice
4. Model selection

Experimental observations are treated as a separate experimentation track.

Python API
==========

Summary Mode
------------

Use ``map_text_to_observation`` to get the full structured mapping object:

.. code:: python

   from kmds.utils.natural_language_observation import map_text_to_observation

   mapping = map_text_to_observation(
       "The model accuracy dropped by 5% after pruning on 2026-04-20."
   )

   print(mapping.workflow_family)
   print(mapping.observation_type)
   print(mapping.extracted_entities.metric)
   print(mapping.extracted_entities.value)
   print(mapping.validation_passed)

Use ``summarize_observation_text`` when you want a compact human-readable
summary:

.. code:: python

   from kmds.utils.natural_language_observation import summarize_observation_text

   summary = summarize_observation_text(
       "Missing values were observed in the customer_age field during intake validation."
   )
   print(summary)

Generate Python Logging Code
----------------------------

Use ``build_observation_python_code`` to generate a code snippet that follows
the existing KMDS ontology classes and properties:

.. code:: python

   from kmds.utils.natural_language_observation import (
       build_observation_python_code,
       map_text_to_observation,
   )

   mapping = map_text_to_observation(
       "We engineered a rolling 7 day demand feature from timestamped order counts."
   )
   code = build_observation_python_code(mapping)
   print(code)

Generate JSON-LD
----------------

Use ``build_observation_jsonld`` to generate a JSON-LD structure that only uses
existing KMDS schema properties:

.. code:: python

   from kmds.utils.natural_language_observation import (
       build_observation_jsonld,
       map_text_to_observation,
   )

   mapping = map_text_to_observation(
       "We chose XGBoost after comparing several tree ensembles on validation AUC 0.91."
   )
   json_ld = build_observation_jsonld(mapping)
   print(json_ld)

Log Mode
--------

Use ``log_text_as_observation`` to validate and save the observation into a KMDS
knowledge base:

.. code:: python

   from kmds.utils.natural_language_observation import log_text_as_observation

   result = log_text_as_observation(
       text="Missing values were observed in the customer_age field during intake validation.",
       workflow_name="support_reporting_intake",
       project_file_path="./support_reporting_intake.xml",
       project_mode="create",
       workflow_type="application",
   )

   print(result.mapping.observation_type)
   print(result.project_file)

Update an existing KMDS knowledge base:

.. code:: python

   result = log_text_as_observation(
       text="We engineered a rolling 7 day demand feature from timestamped order counts.",
       workflow_name="support_reporting_intake",
       project_file_path="./support_reporting_intake.xml",
       project_mode="update",
   )

CLI Usage
=========

The feature is available as ``kmds-observe``.

Summary Mode As Text
--------------------

.. code:: bash

   kmds-observe \
     --text "Missing values were observed in the customer_age field during intake validation." \
     --mode summary

Summary Mode As JSON
--------------------

.. code:: bash

   kmds-observe \
     --text "The model accuracy dropped by 5% after pruning on 2026-04-20." \
     --mode summary \
     --output-format json

Summary Mode From A File
------------------------

.. code:: bash

   kmds-observe \
     --text-file ./observation.txt \
     --mode summary \
     --output-format json

Log Mode: Create A New Project
------------------------------

.. code:: bash

   kmds-observe \
     --text "Missing values were observed in the customer_age field during intake validation." \
     --mode log \
     --workflow-name "support_reporting_intake" \
     --project-file ./support_reporting_intake.xml \
     --workflow-type application \
     --create-project

Log Mode: Update An Existing Project
------------------------------------

.. code:: bash

   kmds-observe \
     --text "We engineered a rolling 7 day demand feature from timestamped order counts." \
     --mode log \
     --workflow-name "support_reporting_intake" \
     --project-file ./support_reporting_intake.xml \
     --update-project

Log Mode As JSON
----------------

.. code:: bash

   kmds-observe \
     --text "We chose XGBoost after comparing several tree ensembles on validation AUC 0.91." \
     --mode log \
     --workflow-name "support_reporting_intake" \
     --project-file ./support_reporting_intake.xml \
     --update-project \
     --output-format json

Notebook Usage Pattern
======================

You can use the mapper inside notebooks without switching to the CLI. This is
useful when you want one observation to remain natural-language driven while the
rest of the notebook continues to use manual ontology operations.

.. code:: python

   from kmds.ontology.kmds_ontology import ExploratoryObservation
   from kmds.utils.natural_language_observation import map_text_to_observation

   nl_mapping = map_text_to_observation(
       "Ticket creation and closed timestamps have inconsistent datetime formats, so they must be normalized before calculating time to resolution."
   )

   e4 = ExploratoryObservation(namespace=onto)
   e4.finding = nl_mapping.finding
   e4.finding_sequence = observation_count
   e4.exploratory_observation_type = nl_mapping.observation_type
   e4.intent = nl_mapping.intent
   exp_obs_list.append(e4)

Validation Behavior
===================

KMDS rejects vague inputs that do not provide enough structure for a valid
observation. Examples of invalid input include very short or underspecified
statements such as:

.. code:: text

   Looks better now

Typical validation checks include:

1. The text must be long enough to be meaningful
2. The text must contain enough context to classify into an existing KMDS type
3. The text should expose at least one structured element such as a metric,
   value, timestamp, or affected component
4. Model-selection observations should contain a measurable outcome

Outputs and Return Values
=========================

``map_text_to_observation`` returns a structured mapping object with:

1. KMDS observation family
2. KMDS observation type
3. Ontology class and property names
4. Extracted entities
5. Validation status and validation errors
6. Classification confidence

``log_text_as_observation`` returns a result object with:

1. The structured mapping
2. The project file path written to
3. The workflow name used
4. The action taken, create or update
5. The JSON-LD payload
6. The generated Python logging code