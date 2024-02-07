## Knowledge Management for Data Science

### What is this tool used for?

This tool is used for knowledge management in data science. In software design, conceptual domain models inform lower level models. In data science work, experiments yield knowledge that inform modelling choices. Data science models are almost always informed by a variety of analysis experiments. Experimentation and organization of knowledge artifacts supporting modeling decisions is a requirement for reproducible data science models and improving model quality and performance.

Please see [knowledge application development context](../feature_documentation/knowledge_management_in_DS.md) for a description of a typical knowledge application development setting.

### Why do you need this tool?

The above narrative suggests that ability to retrieve knowledge about experiments and historical models in an adhoc manner is critical in data science. It is. It is also grossly underserved. Knowledge management tools for domain specific models exist, knowledge management tools for dev-ops and ML-Ops exist, but tools for analytics and model development are siloed. So analysts and data scientists often have to go to experiment tools or data catalogs or ML-Ops tools to fetch information they need to develop a model. The next time they are involved in the next iteration of this model, the contextual information that informed the development of this model if often lost and the development team, possibly with new team members, have the task of guessing this contextual information again. This library is a step in that direction.

### Who would use this tool?

This tool is for data scientists and data analysts.

### How do you use this tool?

1. You install this library along with the other python dependecies you need for your analysis task.
2. Decide on a workflow for your analytic or machine learning task. Please see the [the knowledge application pipeline](../feature_documentation/km_app_pipeline.md) document for details of the workflows available. Examples for each of these workflows are provided.
3. A work flow consists of exploratory, data representation and modelling phases. As the analyst works through each of this phases, they decide on the facts they want to document. They collect the facts, tag and order them as a list and then call the API to record them in the knowledge base.
4. When an analyst needs to look up the details of a particular project task, they search the knowledge base. At present, the API supports logging and retrieval of information. Search interfaces, for example with LLM's can be added once the data is available.

### Open Source

This tool is open source. If you have a feature that you would like to submit, thank you, submit a PR and we can take from there.
