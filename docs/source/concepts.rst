Concepts
#########
This section contains the description of concepts used in documenting analytics and machine learning use cases with KMDS.

The Knowledge Management Workflow Context
*******************************************
In a typical enterprise setting we have business or organizational applications that customers and employees interact with. These interactions generate business operational data that is subsequently cleaned and transformed for various analytical or machine learning projects. A schematic of this process is available in `the repository <https://github.com/rajivsam/KMDS/blob/main/feature_documentation/knowledge_management_in_DS.md>`_ . The operational data is usually transformed to the needs of each analytic or machine learning use case. This transoformed representation is the *data representation* for the specific use case. Data representations are developed by knowledge workers, such as business analysts, and technical staff members such as data engineers and data scientists. The correct data representation for a particular use case can evolve over time because there is a *discovery* aspect to data analysis and data science work. Baselining representations and documenting the rationale for the changes and evolution of *data representations* is important to facilitate quick implementation iterations. This is what KMDS can help with.


Workflows
*********
A workflow is a sequence of processing tasks to develop a product for your use case. A product can be a report, a model, a set of features or other data products that you can think of. Typically, in a data science setting, we are interested in developing either an *analytics workflow* or a *machine learning* workflow. Typically in an analytics workflow, the data set is fixed, there is a specific set of exploration questions and the computational approach to get the answers to these questions are established. In contrast, a machine learning workflow may need principled experimentation to accomplish a goal. See `this video <https://www.youtube.com/watch?v=dcXqhMqhZUo>`_ from IBM for more details. In each workflow, the tasks performed can be categorized as either *exploratory*, *data representation*, or, *modeling* based on the nature of the processing performed by the task. See `the workflow typs page in the repository <https://github.com/rajivsam/KMDS/blob/main/feature_documentation/km_app_pipeline.md>`_ for more information.

Observation Logging
*******************
The following are guidelines for what must be captured as part of documenting a workflow.

1. In general, all decisions that change input data or data representations need to be logged with documentation that makes it possible to reproduce these changes. In other words, it is possible for data scientists to reproduce the intermediate data artifacts from the input data by following the logged documentation.
2. The rationale for making modelling choices and the experimental pipelines that informed the rationale should be clearly logged with documentation.
3. Methodology to evaluate task performance must be logged.
4. Assumptions for modelling must be logged.

Glossary of Observation Types
******************************

The tasks within a workflow can be categorized as *exploratory*, *data representation* or *modeling* depending on the nature of the task performed. A description of these types and guidelines for logging observations belonging to these types are prvoided in `the observation glossary <https://github.com/rajivsam/KMDS/blob/main/feature_documentation/glossary_observation_types.md>`_.

Knowledge Graphs
*****************
The developed documentation is stored as an *RDF* graph. This graph can be shared between workflows. In otherwords, the following scenarios are possible:
1. You could start with an exploratory workflow, save it, load the exploratory workflow in a notebook where you ware evaluating different data representations for a use case, once you have determined a suitable data representation you can update the workflow with your observations from data representation experimentation and save the workflow. You can then load the workflow with observations from exploratory data analysis and data represenations in a notebook where you are performing modeling experiments. Once you have determined a suitable model for your use case, you can update the workflow with your observations from modeling. After completing the modeling phase to your satisfaction, you can save the workflow with the documentation to a network location and then load it and review your observations.

2. For workflows that require extensive experimentation, you can create separate workflows for experimentation and then indicate that your use case workflow depends on these experiments. 

Examples of both these scenarios are provided. The repository contains a page explaining the implementation steps for managing the life cycle of the `knowledge graph <https://github.com/rajivsam/KMDS/blob/main/feature_documentation/ontology_management.md>`_ .







   