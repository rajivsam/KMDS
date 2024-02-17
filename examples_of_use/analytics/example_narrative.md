![](images/kmds_logo_resized.jpg)

<div style="text-align: justify">

## An Example of Using KMDS in an Analytics Use Case

An example of using KMDS in an analytics use case is illustrated with a real world use case from the retail domain. This is a supplement to implement the [the recipe](../workflow_recipe.md) for an analytics use case. The data for this example comes from IT incident management. The data pertains to ticket resolution activity at an enterprise service help desk The data is available from the [UCI machine learning repository](https://archive.ics.uci.edu/dataset/498/incident+management+process+enriched+event+log). The data contains details of ticket resolution activity at the help desk. A ticket is submitted by a customer, it is then assigned to a support group. A staff member from the support group works on the ticket, resolves it and closes the ticket. The task description for this use case is provided below.

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

There are two sub-stages in modelling:

### Modelling Choices:

In this phase you explore and evaluate indirect modelling choices related to developing a model that accomplishes the task goal. Some examples of indirect modelling choices:

1. Feature Engineering choices - for example do you want to use an auto-encoder to develop a new representation for your modelling task.
2. Hyper-parameter choices in support of specific modelling choices. For example, do you want to use a specific kernel for your kernel learning method. Do you want to use a specific decision tree height parameter
   Note that these choices can be informed by other knowledge extraction experiments. These knowledge extraction experiments have the explicit goal of informing the model selection approaches used in this pipeline.

For this example, the modelling choices are as follows. The _daily sales representaion_ , as computed initially is high dimensional. A review of the bottom left corner of the above figure shows that there are 3092 items in the inventory. A review of the contribution of each inventory item to the quaterly sales revenue exhibits a power law type curve. Over two thirds of the inventory items do not contribute to the revenue generated from sales in the first quarter. We remove these items from the daily sales representation. This is a modelling choice that simplifies the problem we are trying to model - that of characterizing the shopping activity of the shoppers at the store succintly and extracting patterns of shopping behavior from it.  After removing these rendundant items from the daily sales representation we have a much smaller daily representation. We then apply Principal Component Analysis to reveal a small set of store inventory items that can account for most of the shopping activity in the store during the first quarter of 2010. See [this notebook](/examples_of_use/machine_learning/example_ml_modelling_phase_mc.ipynb) for details of the implementation.

### Model Selection

In this phase you explore the modelling approaches you want to evaluate towards accomplishing your task goal. As discussed in the previous paragraph, we will use Principal Components Analysis for this purpose. There are multiple techniques to summarize datasets. The choice of the approach depends on the application and practical considerations such as schedule and cost. In this work, we are establishing a baseline, so we use a standard technique. The observations we make during modelling are noted and logged using the api. See [this notebook](/examples_of_use/machine_learning/example_ml_modelling_phase_ms.ipynb) for details of the implementation.

## Retrieving Logged Information

Information logged durring analysis tasks can be retrieved using the API, see [this notebook](/examples_of_use/machine_learning/example_ml_observations_report.ipynb) for how this is done for the provided example.
