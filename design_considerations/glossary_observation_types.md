## Types of Observations


### Exploratory Observations
These observations document the findings of an analyst reviewing a _raw_ dataset in preparation for a specific analysis task. It should be noted that exploratory data anlysis is usually performed in the context of a goal or a task. Usually, there are problems in acquiring or processing the data(_noise_). There are cases when you do get reliable data without these errors, so noise in the data is a use case specific property. Sometimes, there are problems introduced by the statistical properties of the data (_outliers_).

### Data Representation Observations
These are observations that document the findings of an analyst preparing the _raw_ data, usually, after the _exploratory data analysis_ has been performed. The raw data received may not be in a form that is amenable to the analysis that we wish to perform. The analyst may want to _transform_ the data to a form suitable for the analysis task. The observations made by the analyst to document and communicate the rationale and assumptions in developing these transformed representations of the data are what are captured as _Data Representation Observations_.

### Modelling Observations
The analyst may consider a set of modelling approaches to develop a model to accomplish a use case goal. The observations that capture the rationale and assumptions for considering a specific set of approaches and the salient aspects of the results in each approach are captured with _Model Selection Observations_. Each modelling approach may further require the selection of parameters specific to the modelling approach. The observations documenting these choices and the rationale and assumptions for making them are captured with _Model Choice Observations_.

### Experimental Observations
Experimental Observations are used to capture the details of the experiment that an analyst is performing with the workflow. This should capture the description of the goals of the experiment, assumptions, observations, results and conclusions. This set of features is work in progress and will be illustrated with an example in a future release.


See the ```tagging.tag_types.py``` module for further resolution of the types available in each category. The example notebooks should illustrate how these types are specified when observations are recorded. The observations must be ordered while recording them. This is done by specifying a sequence number for the observation.
