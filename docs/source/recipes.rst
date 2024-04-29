
Recipes
########

This section contains descriptions of recipes used to illustrate KMDS concepts with real world use cases. Please see `the workflow documentation guideline <https://github.com/rajivsam/KMDS/blob/main/examples_of_use/workflow_recipe.md>`_ for the details of the steps involved in integrating KMDS into your analytics and machine learning workflows. The examples discussed in this section follow this process. An example may illustrate a specific set of features and concepts. These are provided in the description.

Data Analysis
*************

Generating a Data Quality report
================================

When you receive a new dataset containing the raw data that is to be used for developing your product, one of the first things you want to do is to develop a baseline profile of the data quality of the raw dataset. This can be done with a notebook for the first iteration of modeling and subsequent data increments can possibly be analyzed with a workflow tool such as *argo* or *prefect*. An example showing how *data quality* can be documented with a workflow tool (*prefect*) is shown in the `data quality report example <https://github.com/rajivsam/kmds_recipes/wiki/Baseline-Data-Quality-Report>`_. The process of logging the data quality with a notebook is identical to what is done with the workflow tool except that the analysis process is initially manually performed. 


Analytics
**********

Developing and Documenting an Analytics Workflow
=================================================

There are two examples illustrating the use of KMDS to develop an analytics workflow. One example uses data from an incident management. The details are provided in the `incident management analytics narrative <https://github.com/rajivsam/KMDS/blob/main/examples_of_use/analytics/example_narrative.md>`_. The other example uses data from finance. The details are provided in the `SBA 7a loan repayment analysis narrative <https://github.com/rajivsam/kmds_recipes/wiki/A-simple-KMDS-analytics-reporting-project>`_.

Machine learning
*****************

Developing and Documenting a Machine Learning Workflow
=======================================================
There are two examples illustrating the use of KMDS to develop a machine learning workflow. One example uses data from retail. This example provides an example of using KMDS to document an *unsupervised* learning task. The details are provided in `the retail unsupervised learning narrative <https://github.com/rajivsam/KMDS/blob/main/examples_of_use/machine_learning/example_narrative.md>`_ . Another example uses data from finance. This example serves to illustrate the details of using KMDS to document a *supervised* learning task. The details are provided in `the 7a loan charge-off modeling narrative <https://github.com/rajivsam/kmds_recipes/blob/main/recipes/machine_learning/imbalanced_cost_based_learning/7a_chargeoff_modelling.rst>`_.








