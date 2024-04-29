
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

Connecting Workflows
=====================
It is possible to perform specific phases or specific tasks as separate workflows and then use them in your modeling workflow. For example, you may want to develop and refine features for your task in a separate workflow and then use those features in your modeling workflow. To do this you indicate that that the modeling workflow depends on the feature engineering workflow. Then team members reviewing modeling activity development know that the modeling workflow has a dependency that must be executed first prior to embarking on model development activity. This idea is illustrated with `7a loan charge off modeling example <https://github.com/rajivsam/kmds_recipes/blob/main/recipes/machine_learning/feature_engineering/feature_engg_sba_7a_chargeoffs.md>`_ . A feature engineering workflow that refines attributes and develops a better set of features to predict loan charge off's is developed first. This is then used in a `modeling notebook <https://github.com/rajivsam/kmds_recipes/blob/main/recipes/machine_learning/imbalanced_cost_based_learning/7a_WOE_chargeoff_modelling.rst>`_. 

Feature Profiling
==================
As part of model development, analysts often want an assessment of the relevance and impact of the available features on the modeling task of interest. For example we may want to understand which features are most relevant in determining a target label or response in a supervised learning task. This can be determined using model inspection. We may also want to understand the nature of the relationship between the target response and the feature. For example, we may want to know if the predictor shares a non-linear relationship with the target in a regression problem or if the decision boundary is non-linear in a classification problem. This kind of characterization of the features in relation to the learning task of interest is called a *feature profile* for the task. An example of a feature profile is provided using *sensor data*. The details of developing a feature profile for this dataset is available in the `feature profiling task narrative <https://github.com/rajivsam/kmds_recipes/wiki/Feature-Profile>`_.

Data Profiling
==============

A data profile is the characaterization of the dataset in relation to the learning task. *Heterogeniety* is often the motivation for creating a *data profile*. The *heterogeniety* is in the context of the learning task that we are interested in performing. The particular form *heterogeniety* depends on the type of data that we are analyzing. In a time series dataset, *heterogeniety* can manifest as different components such as the *trend* and *seasonality* that occur in the data. In cross-sectional data, it is possible that different regions of your dataset have different sets of relationships between the predictor and response. In such a dataset, trying to fit one hypothesis to the entire dataset may yield poor results. A data profile tells us the kind of *heterogeniety* we must account for during modeling. An example of a data profile for time series data is provided for an `economic dataset <https://github.com/rajivsam/kmds_recipes/wiki/Data-Profile-for-a-time-series-using-Singular-Spectrum-Analysis>`_. 

Data Annotation
================
Data products and models are first class products today. Companies can produce features such as word, text, or, image embeddings for consumers. An example of producing a `data product <https://github.com/rajivsam/kmds_recipes/blob/main/recipes/machine_learning/data_annotation/data_annotation_7a_charge_off_probs.md>`_ is provided. This example categorizes the customers make 7a loan payments in 2023 into "good", "average" and "poor" credit risk buckets. The provided example illustrates how KMDS can be used to document data annotation workflows.












