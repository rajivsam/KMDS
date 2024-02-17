<div style="text-align: justify">

## An Example of Using KMDS in a Machine Learning Use Case

An example of using KMDS in a machine learning use case is illustrated with a real world use case from the retail domain. This is a supplement to implement the [the recipe](../workflow_recipe.md) for a machine learning use case. The data for this use case is a set of transactions at an online retail store based in the UK. The data is available from the [UCI machine learning repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii). The data spans transactions at the store over the years 2010 through 2011. The task description for this use case is given below.

### Task Description

Let's set the date for this exercise to be the first week after the business quarter in the year 2010. The store management would like to understand the shopping activity in the store in the previous quarter. The store is visited by many customers and there is variation in the items that are purchased in the store every day. They would also like to apply data science to summarize the shopping activity in the store in the first quarter. This would help them understand customer taste in that time period. This kind of analysis can inform inventory planning tasks for the store. They have not done developed a model like this before. They would like to approach the model development guided by principled experiments to understand the characteristics of the data. This phase will be modelled with the Knowledge Extraction Experiment Workflow. This sketch illustrates how KMDS can be used to log data from an experimental workflow.

## Data Processing Approach

1. The raw data set covers the period 2010 and 2011. We only need the first quarter data for this analysis. So we subset the data corresponding to this period. This [notebook](/examples_of_use/machine_learning/example_ml_data_subsetting.ipynb) has the code for doing this. The original dataset can be obtained from the [UCI machine learning repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii)
2. The modelling approach is illustrated on the data for Q1 2010. The data for Q2 2010 is also provided and can be used to evaluate or replicate the approach on a new dataset. This is the analysis that would be performed by the data science team at the end of the second quarter. For those interested in exploring this tool, replicating the analysis for the first quarter on the data from the second quarter may be a good way to gain familiarity with the tool.

## Exploratory Data Analysis

Exploratory Data Analysis performs the following tasks:

1. It identifies the issues in the raw data set that prevent us from developing an understanding of the raw data, for example, we can have mixed types in raw data set. A price could have a string value. This prevents us from using basic statistical tools to analyze the data. Such issues are called _attribute noise_ in the notebooks.
2. It removes _attribute noise_
3. Given our task description, we evaluate transformations of the raw data that can help us achieve the task goal. Since our goal is to understand customer behavior in the first quarter. We could compute the sales of each of the store inventory items for each day of the first quarter (there are 75 business days in the first quarter). We could then analyze this sales per day representation from a similarity view point and evaluate if we can find patterns of daily purchases at the store during the first quarter.  In other words, we _explore_ ways to develop _data representations_ that can help us achieve our task goals.
4. Details of the issues identified and the processing steps to resolve them are captured as _knowledge_ and logged.
5. Details describing the approaches that are evaluated to develop _data representations_ that can help us with the analysis task are logged.
6. See [this notebook](/examples_of_use/machine_learning/example_ml_eda_phase.ipynb) for the implementation.

## Data Representation

1. In the raw dataset, each line represents a line item in a sales transaction that occured in the store. If you went to the online store and purchased five types of items, then your purchase (transaction) would generate one line in the dataset for each of the five item types, so your purchase would generate five lines. This information for the first quarter of 2010 is the _raw data representation_. A sample is shown in the image below.

![](../../images/raw_data_rep.png)

2. As discussed in the exploratory data section, compute a representation where we aggregate all the sales transactions per day and then represent the daily sales for the quarter as a vector that has length equal to the size of the inventory. An element of the vector represents the daily sales corresponding to the inventory item coordinate. A sample of this representation is shown below. This representation is called the _daily sales representation_ in this discussion.

![](../../images/q1_sales_summary.png)

As part of capturing knowledge about data representations, the above two statmements are logged. See [this notebook](/examples_of_use/machine_learning/example_ml_data_rep_phase.ipynb) for the implementation.

## Modelling

As discussed in [Modelling Observations](../../feature_documentation/glossary_observation_types.md), in the modelling stage we evaluate models used to achieve the task or use case goals. In this example, the goal is to explain the variation in daily sales succintly so that we can understand the inventory items that have active sales activity in the first quarter. To do this we use Principal Component Analysis (PCA) in this example. There are several ways to explain the variation in sales activity. The goal of this example is to illustrate how observations in a machine learning workflow are captured with KMDS rather than a critical analysis of the modelling approach to solve this proble. Nevertheless, PCA is a good baseline and does yield useful information that helps us with the goals of this task. So observations made about the application of PCA would be recorded as _Model Selection Observations_. It turns out that most of the store inventory is inactive in the first quarter. These are inventory items that did not contribute significantly to the revenue generated in the first quarter. We can drop these inventory items to reduce the sparsity in the data representation. The analysis and observations pertaining to doing this are recorded as _Modelling Choice Observations_ . This observation supports our modelling decision to use PCA. See [this notebook](/examples_of_use/machine_learning/example_ml_modelling_phase_mc.ipynb) for details of the implementation for modelling choice observations. See [this notebook](/examples_of_use/machine_learning/example_ml_modelling_phase_ms.ipynb) for details of model selection  observations.


## Retrieving Logged Information

Information logged durring analysis tasks can be retrieved using the API, see [this notebook](/examples_of_use/machine_learning/example_ml_observations_report.ipynb) for how this is done for the provided example.
