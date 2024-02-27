[![DOI](https://zenodo.org/badge/753950832.svg)](https://zenodo.org/doi/10.5281/zenodo.10695270)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Documentation Status](https://readthedocs.org/projects/kmds/badge/?version=latest)](https://kmds.readthedocs.io/en/latest/?badge=latest)
<p align="center">
  <img width="460" height="300" src="https://github.com/rajivsam/KMDS/blob/main/images/kmds_logo_resized.jpg">
</p>

## Knowledge Management for Data Science

### What is this tool used for?

This tool is used for knowledge management in data science. In software design, conceptual domain models inform lower-level models. In data science work, experiments yield knowledge that informs modeling choices. Data science models are almost always informed by a variety of analysis experiments. Experimentation and organization of knowledge artifacts supporting modeling decisions is a requirement for reproducible data science models and improving model quality and performance.

Please see [knowledge application development context](https://github.com/rajivsam/KMDS/blob/main/feature_documentation/knowledge_management_in_DS.md) for a description of a typical knowledge application development setting.

### Why do you need this tool?

The above narrative suggests that ability to retrieve knowledge about experiments and historical models in an adhoc manner is critical in data science. It is. It is also grossly underserved. Knowledge management tools for domain specific models exist, knowledge management tools for dev-ops and ML-Ops exist, but tools for analytics and model development are siloed. Information gets fragmented over time. So analysts and data scientists often have to go to experiment tools, data catalogs or ML-Ops tools to fetch information they need to develop a model. In a subsequent iteration of this model, the contextual information that informed the development of this model is often lost, and the development team, possibly with new team members, have the task of reconstructing this contextual information again. This library is a step in fixing this problem. The central idea is to organize tasks in terms of a sequence of steps that are pretty standard in data analysis work and capture knowledge in context while these tasks are performed.

### How is it related to process guidelines and vocabularies for machine learning?
Initiatives such as [CRISP DM](https://www.datascience-pm.com/crisp-dm-2/) provide guidelines and processes for developing data science projects. Projects such as [Open ML](https://openml.github.io/openml-python/main/index.html) provide semantic vocabulary standardization for machine learning tasks. These are excellent tools. However, the guidelines they provide are task focussed. The gap between a conceptual idea and the final, or, even candidate data science tasks for a project is filled with many assumptions and experimental evaluations. The information in these assumptions and experimental evaluations is what this tool aims to capture. There is also an ordering to these assumptions and experimental evaluations. This is also what this tool aims to capture.

### Who would use this tool?

This tool is for data scientists and data analysts.

### How do you use this tool?

1. You install this library along with the other python dependecies you need for your analysis task
2. Review the [basic recipe](https://github.com/rajivsam/KMDS/blob/main/examples_of_use/workflow_recipe.md) for capturing your observations.
3. Review [the templates section](https://github.com/rajivsam/KMDS/blob/main/examples_of_use/workflow_recipe.md) to find the example relevant to you. For analytics projects, review the analytics template. For machine learning projects, review the machine learning template.
4. Start using the tool in your projects using the information from your review of the above two steps.

### Licensing and Feature Questions

1. The tool is open source with an [apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0.txt)
2. If you are interested in the following features, please set up a [meeting](https://calendly.com/rajiv-sambasivan/help-with-kmds-feature) with me:
   1. Help with a data analysis task for your use case
   2. Developing an ontology based solution similar to the above for your specific use case.
   3. Customizing this tool with other extensions, for example to integrate a feature store or meta-data management tool that you use in your data science tool stack.

3. If this problem resonates with you as a developer  and you would like to contribute, submit an issue and if the feature makes sense we can discuss the possiblity of submitting a PR for it. Of course, you can fork this repository and use it per the licensing information. Thank you for your interest.
