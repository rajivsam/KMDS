from enum import Enum

class ExploratoryTags(str, Enum):
    """ Tags to capture the exploratory observation type

    Args:
        str (_type_): string type tag
        Enum (_type_): string type tag
    """
    RELEVANCE_OBSERVATION = "Relevance Observation" 
    DATA_QUALITY_OBSERVATION = "Data Quality Observation"

class DataRepresentationTags(str, Enum):
    """ Tags to capture the data representation observation type
    Args:
        str (_type_): string type tag
        Enum (_type_): string type tag
    """
    FEATURE_ENGG_OBSERVATION = "Feature Engineering Observation"
    DATA_TRANSFORMATION_OBSERVATION = "Data Transformation Observation"

class ModellingChoiceTags(str, Enum):
    """ Tags corresponding to Modelling choice observation type
    Args:
        str (_type_): string type tag
        Enum (_type_): string type tag
    """
    MODELLING_CHOICE_OBSERVATION = "Modelling Choice Observation"
    MODELLING_ASSUMPTION_OBSERVATION = "Modelling Assumption Observation"

class ExperimentationTags(str, Enum):
    """ Tags corresponding to experimentation observation type
    Args:
        str (_type_): string type tag
        Enum (_type_): string type tag
    """
    HYPOTHESIS_STATEMENT = "Hypothesis Statement"
    EXPERIMENTAL_OBSERVATION = "Experimental Observation"
    EXPERIMENTAL_CONJECTURE = "Experimental Conjecture"
    RESULT_SUMMARY = "Experimental Result Summary"

class ModelSelectionTags(str, Enum):
    """ Tags corresponding to Model Selection observation type
    Args:
        str (_type_): string type tag
        Enum (_type_): string type tag
    """
    MODEL_SELECTION_STATEMENT = "Model Selection Statement"
    MODEL_SELECTION_SETUP_DESCRIPTION = "Model Selection Setup Description"
    MODEL_SELECTION_OBSERVATION = "Model Selection Observation"
    MODEL_SELECTION_RESULT_SUMMARY = "Model Selection Result Summary"

