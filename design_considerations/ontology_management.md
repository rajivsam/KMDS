## Ontology Management

## Why does KMDS need an ontology?
Most business problems have a vocabulary and a context within which a problem is defined and solved. Ontologies give you a framework for doing this.
## What is the KMDS ontology?
The actual implementation of the ontology is in the ontology subfolder of the source code. It is based on the [owlready2](https://pypi.org/project/Owlready2/) library.
The vocabulary is based on the basic workflow in most data science projects, you have incremental stages for (1) Data Exploration (2) Data Representation (3) Modelling (4) Model Evaluation . Experimentation is recognized as an important workflow in modern data science. So there are two workflow types provided, one for application development and one for experimentation.

The basic workflow in managing the ontology for a workflow stage is as follows:
1. Load the ontology. If this is the Exploratory Data Analysis Stage, the base ontology that comes with the package is loaded.
2. Use the loaded ontology as the namespace to add the observations for each stage.
3. Save the updated ontology to disk or network location. 
4. To record observations in a subsequent stage, go back to step 1 and start with the ontology saved in step 3.

This is the sequence of operations to record observations into workflows in the examples. 