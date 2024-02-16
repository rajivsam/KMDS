## Summary of Steps in using KMDS

1. Decide the workflow. Are you going to use a fixed, pre-defined algorithm for either learning or computation? Then use the Knowledge Application Workflow. Otherwise, if you need experimentation use the Knowledge Extraction Experiment workflow to determine what you need to nail before developing the final model with the Knowledge Application Workflow. Knowledge Experiment Workflows inform other Knowledge Experiment Workflows, or, a Knowledge Application Workflow.
3. Work through the phases. There is an ordering of the phases. The exploratory phase informs the knowledge representation phase that is used in the modelling phase.
4. Track observations and observation types.
5. Order your observations. In each phase (exploratory, data representation. modelling choices or model selection), assign a sequence number to each observation. Collect your observations in groups - exploratory, data representation. modelling choices or model selection.
6. Write the observations for each group using the meta-data api.
7. When you need information pertaining to a particular project activity, you search for the activity in the knowledge base within the scope of the phase of the activity falls into - exploratory data analysis, data representation, modelling. Please see [this example notebook](machine_learning/example_ml_observations_report.ipynb) for an illustration. At present, the API supports logging and retrieval of information. Search interfaces, for example with LLM's can be added once the data is available. The tool uses an ontology for knowledge representation. So it should be possible to perform task specific reasoning on it.


## Guidelines for picking a workflow and examples
1. Please see the [the knowledge application pipeline](../feature_documentation/km_app_pipeline.md) document for details of the workflows available. 
4. If you need a machine learning workflow, review the [machine learning example](machine_learning/example_narrative.md) to get familiar with the recipe for capturing observations in machine learning based project.
5. If you need an analytic workflow, review the [analytic task example](analytics/example_narrative.md) to get familiar with the recipe for capturing observations in an analytics project.