![](images/kmds_logo_resized.jpg)

<div style="text-align: justify">

## An Example of Using KMDS in an Analytics Use Case

An example of using KMDS in an analytics use case is illustrated with a real world use case from the retail domain. This is a supplement to implement the [the recipe](../workflow_recipe.md) for an analytics use case. The data for this example comes from IT incident management. The data pertains to ticket resolution activity at an enterprise service help desk. The data is available from the [UCI machine learning repository](https://archive.ics.uci.edu/dataset/498/incident+management+process+enriched+event+log). The data contains details of ticket resolution activity at the help desk. A ticket is submitted by a customer, it is then assigned to a support group. A staff member from the support group works on the ticket, resolves it and closes the ticket. The task description for this use case is provided below.

### Task Description
The help desk administration would like to review and understand the performance of the organization every quarter. For this purpose, it generates the following measures:
1. The time taken to resolve tickets submitted to the help desk for that quarter.
2. The number of tickets closed by each support group for that quarter.
   
   
For this purpose two models are constructed:
   1. Model 1: Calculate the resolution time for each ticket resolved that quarter, obtain a distributional visualization of the resolution times. The characteristics of the distributional visualization should yield information about the resolution activity that quarter. The cumulative distribution of resolution times should yield a probablistic perspective of the resolution time. It helps the administration understand and set service level agreeements. Such a plot can tell the adminstration that x percentage of tickets are resolved in y hours. This not only helps the adminstration set expectations with customers of the help desk, it can also be used to track if the effectiveness of the help desk organization is improving or deteriorating with time.
   2. Model 2: Calculate the number of tickets closed by each support group in the organization. This helps the adminstration understand the ticket load and effectiveness of each support group.
   
## Exploratory Data Analysis

Exploratory Data Analysis performs the following tasks:

1. Select the subset of attributes that are need for this use case
2. Analyze the (subsetted) dataset for data quality
3. Fix attribute noise
4. Write the denoised data for the next phase in the workflow.
5. Log the relevance and noise processing details done as part of exploratory data analysis to KMDS

This is implemented in [](example_analytics_eda_phase.ipynb)

## Data Representation
There are two models that are developed, as a result there are two data representations that are needed.

1. Data Representation 1: Starting the raw data from the exploratory data analysis phase, compute a new derived attribute (feature engineering) called _resolution time_ that captures the time to resolve a ticket. This is the time difference between the creation and the closing of the ticket. This is implemented in [](example_analytics_data_rep_1.ipynb)
2. Data Representation 2: Starting with the raw dataset from exploratory data analysis, count the number of tickets for each support group (this a group by on the support group attribute). This is implemented in [](example_analytics_data_rep_model_selection2.ipynb)

## Modelling
Since there are two models that are needed in this use case, there are two sets of model selection observations, with one set of observations for each model. There is parameter selection or supporting analysis that we need to document for either of the two models. As a consequence, there are no modelling choice observations. See [this notebook](example_analytics_model_selection_1.ipynb) for the details of the implementation for Model 1. See [this notebook](example_analytics_data_rep_model_selection2.ipynb) for the details of the implementation for Model 2.


## Retrieving Logged Information

Information logged durring analysis tasks can be retrieved using the API, see [this notebook](example_analytics_observations_report.ipynb) for how this is done for the provided example.
