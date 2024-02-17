## Ontology Management

The basic workflow in managing the ontology for a workflow stage is as follows:
1. Load the ontology. If this is the Exploratory Data Analysis Stage, the base ontology that comes with the package is loaded.
2. Use the loaded ontology as the namespace to add the observations for each stage.
3. Save the updated ontology to disk or network location. 
4. To record observations in a subsequent stage, go back to step 1 and start with the ontology saved in step 3.

This is the sequence of operations to record observations into workflows in the examples. 