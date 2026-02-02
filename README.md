[![DOI](https://zenodo.org/badge/753950832.svg)](https://zenodo.org/doi/10.5281/zenodo.10695270)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Documentation Status](https://readthedocs.org/projects/kmds/badge/?version=latest)](https://kmds.readthedocs.io/en/latest/?badge=latest)
<p align="center">
  <img width="460" height="300" src="https://raw.githubusercontent.com/rajivsam/KMDS/main/images/kmds_logo_resized.jpg">
</p>

## Knowledge Management for Data Science
<div class="callout-left full">


</div>

### What is the tool and why do you need it?

This tool is used for knowledge management in data science. As data scientists, incremental experimentation is a way of life. The problem is we have a lot of them and even small projects accumalate context, decisions and rationale over time. This is not a problem if we have both the need for experimentation (the design question or issue) and the results documented over time, but this tends to be done in an adhoc manner, so when its time to rebuild or revisit a particular question, we can't find the research and the results related to it. This is the need this tool fulfils.

Please see [knowledge application development context](https://github.com/rajivsam/KMDS/blob/main/feature_documentation/knowledge_management_in_DS.md) for a description of a typical knowledge application development setting. Please see [the video](example_documentation/video/Knowledge_Management_for_Data_Science_comp.mp4) for a quick overview.

### How is it related to process guidelines and vocabularies for machine learning?
Initiatives such as [CRISP DM](https://www.datascience-pm.com/crisp-dm-2/) provide guidelines and processes for developing data science projects. Projects such as [Open ML](https://openml.github.io/openml-python/main/index.html) provide semantic vocabulary standardization for machine learning tasks. These are excellent tools. However, the guidelines they provide are task focussed. The gap between a conceptual idea and the final, or, even candidate data science tasks for a project is filled with many assumptions and experimental evaluations. The information in these assumptions and experimental evaluations is what this tool aims to capture. There is also an ordering to these assumptions and experimental evaluations. This is also what this tool aims to capture.

### Who would use this tool?

This tool is for data scientists and data analysts.

### How do you use this tool?
This version of the tool takes all the recent advances (as of early 2026) into consideration in how this tool is used. This is a python package. It is assumed that you have an API key to a provider. The basic usage scenario is as follows:
1. Install the python package in the environment where you intend to experiment and do your data science analysis.
2. Work through your analysis plan for your model development or experiment. The tool will not offer help with how your analysis or experiment will be done. It assumes you are the expert and you know how to do this. Of course, you can use __Jupyternaut__ or a similar generative AI tool to generate your code for you.
3. As you work through your exploratory data analysis, data representation and modeling phases, log your findings to ```kmds```
4. Run a report to fetch the details of your design rationale as needed. To communicate your findings to your team or management, simply export your knowledge base. Point a generative AI tool such as __NotebookLM__ to the export and generate your report, video or other documentation artifact.

### Examples of use
The repository contains two examples of use. One example is from analytics, the other is from machine learning. The notebooks for analytics are in [the analytics example](examples_of_use/analytics) and the notebooks for machine learning are in [the machine learning example](examples_of_use/machine_learning). The analytics example evaluates the effectiveness of ticket resolution help desk. Using ticket resolution data for a particular quarter, Q2 2016, the example illustrates how effectiveness of the organization can be evaluated. The reader can explore the notebooks to see the details of the implementation and details of how findings in each phase of the model building cycle are logged. The findings from the resulting knowledge base can be exported to create materials to communicate the details of the project to team members and management, see [this video](examples_of_use/analytics/Help_Desk_Analytics%20_comp.mp4) and this [infographic](examples_of_use/analytics/usecase_overview_mindmap.png)

The machine learning example illustrates how Principal Components Analysis can be used to summarize the sales activity in an online store for a particular quarter. The reader can view the notebooks under [the machine learning example](examples_of_use/machine_learning) for details of the implementation. As with the analytics example, generative AI tools (Notebook LM in this case) can be used to communicate the findings and results from the knowledge base, see [this infographic](examples_of_use/machine_learning/ml_infographic_kmds.png).

### Licensing and Feature Questions

1. The tool is open source with an [apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0.txt)
2. If you are interested in the following features, please set up a [meeting](https://calendly.com/rajiv-sambasivan/help-with-kmds-feature) with me:
   1. Help with a data analysis task for your use case
   2. Developing an ontology based solution similar to the above for your specific use case.
   3. Customizing this tool with other extensions, for example to integrate a feature store or meta-data management tool that you use in your data science tool stack.

3. If this problem resonates with you as a developer  and you would like to contribute, submit an issue and if the feature makes sense we can discuss the possiblity of submitting a PR for it. Of course, you can fork this repository and use it per the licensing information. Thank you for your interest.
