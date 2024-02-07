from enum import Enum

class ExploratoryTags(str, Enum):
    RELEVANCE_OBSERVATION = "Relevance Observation" 
    DATA_QUALITY_OBSERVATION = "Data Quality Observation"

class DataRepresentationTags(str, Enum):
    FEATURE_ENGG_OBSERVATION = "Feature Engineering Observation"
    DATA_TRANSFORMATION_OBSERVATION = "Data Transformation Observation"

class ModellingChoiceTags(str, Enum):
    MODELLING_CHOICE_OBSERVATION = "Modelling Choice Observation"
    MODELLING_ASSUMPTION_OBSERVATION = "Modelling Assumption Observation"

class ExperimentationTags(str, Enum):
    HYPOTHESIS_STATEMENT = "Hypothesis Statement"
    EXPERIMENTAL_OBSERVATION = "Experimental Observation"
    EXPERIMENTAL_CONJECTURE = "Experimental Conjecture"
    RESULT_SUMMARY = "Experimental Result Summary"

class ModelSelection(str, Enum):
    MODEL_SELECTION_STATEMENT = "Model Selection Statement"
    MODEL_SELECTION_SETUP_DESCRIPTION = "Model Selection Setup Description"
    MODEL_SELECTION_OBSERVATION = "Model Selection Observation"
    MODEL_SELECTION_RESULT_SUMMARY = "Model Selection Result Summary"

