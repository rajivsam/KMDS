<div style="text-align: center;">
    <img width="100%" src="images/kmds_logo_resized.jpg">
</div>

## Knowledge Management for Data Science

### What is this tool used for?

This tool is used for knowledge management in data science. In software design, conceptual domain models inform lower-level models. In data science work, experiments yield knowledge that informs modeling choices. Data science models are almost always informed by a variety of analysis experiments. Experimentation and organization of knowledge artifacts supporting modeling decisions a requirement for reproducible data science models and improving model quality and performance.This tool is used for knowledge management in data science. In software design, conceptual domain models inform lower level models. In data science work, experiments yield knowledge that inform modelling choices. Data science models are almost always informed by a variety of analysis experiments. Experimentation and organization of knowledge artifacts supporting modeling decisions is a requirement for reproducible data science models and improving model quality and performance.

Please see [knowledge application development context](/feature_documentation/knowledge_management_in_DS.md ) for a description of a typical knowledge application development setting.

### Why do you need this tool?

The above narrative suggests that ability to retrieve knowledge about experiments and historical models in an adhoc manner is critical in data science. It is. It is also grossly underserved. Knowledge management tools for domain specific models exist, knowledge management tools for dev-ops and ML-Ops exist, but tools for analytics and model development are siloed. Information gets fragmented over time. So analysts and data scientists often have to go to experiment tools, data catalogs or ML-Ops tools to fetch information they need to develop a model. In a subsequent iteration of this model, the contextual information that informed the development of this model if often lost and the development team, possibly with new team members, have the task of reconstructing this contextual information again. This library is a step in fixing this problem. The central idea is to organize tasks in terms of a sequence of steps that are pretty standard in data analysis work and capture knowledge in context while these tasks are performed.

### Who would use this tool?

This tool is for data scientists and data analysts.

### How do you use this tool?

1. You install this library along with the other python dependecies you need for your analysis task
2. Decide on a workflow for your analytic or machine learning task. Please see the [the knowledge application pipeline](/feature_documentation/km_app_pipeline.md) document for details of the workflows available. [A machine learning example](/examples_of_use/machine_learning/example_narrative.md) and an analytics example is provided.
3. A work flow consists of exploratory, data representation and modelling phases. As the analyst works through each of this phases, they decide on the facts they want to document. They collect the facts, tag and order them as a list and then call the API to record them in the knowledge base.
4. When an analyst needs to look up the details of a particular project task, they search the knowledge base. Please see [this example notebook](/examples_of_use/machine_learning/example_ml_observations_report.ipynb) for an illustration. At present, the API supports logging and retrieval of information. Search interfaces, for example with LLM's can be added once the data is available. The tool uses an ontology for knowledge representation. So it should be possible to perform task specific reasoning on it.

### Licensing and Feature Questions

1. The tool is open source with an [apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0.txt)
2. If you are interested in the following features, please set up a [meeting](https://calendly.com/rajiv-sambasivan/help-with-kmds-feature) with me:
   1. Help with a data analysis task for your use case
   2. Developing an ontology based solution similar to the above for your specific use case.
   3. Customizing this tool with other extensions, for example to integrate a feature store or meta-data management tool that you use with this approach, please set up a [meeting](https://calendly.com/rajiv-sambasivan/help-with-kmds-feature) with
3. You can also set up a [meeting](https://calendly.com/rajiv-sambasivan/help-with-kmds-feature) with me to discuss customizing this tool for your specific project or use case. For example, you may want to integrate this tool with a meta-data management solution or a feature engineering solution.
4. If this problem resonates with you as a developer  and you would like to contribute, submit an issue and if the feature makes sense we can discuss the possiblity of submitting a PR for it. Of course, you can fork this repository and use it per the licensing information. Thank you for your interest.
