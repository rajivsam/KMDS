from owlready2 import *
from typing import List
from enum import Enum
from tagging import *
import os
from utils.path_utils import get_ontology_path



class PipelineType(str, Enum):
    KNOWLEDGE_APPLICATION_WORKFLOW = "Knowledge Application Workflow"
    KNOWLEDGE_EXTRACTION_EXPERIMENT_WORKFLOW = "Knowledge Extraction Experiment Workflow"


# Concept definitions
onto = get_ontology(get_ontology_path()).load()

with onto:
    class Workflow(Thing):
        pass
    class KnowledgeApplicationWorkflow(Workflow):
        pass
    
    class KnowledgeExtractionExperimentationWorkflow(Workflow):
        pass
    
    class description(DataProperty, FunctionalProperty):
        domain = [Workflow]
        range = [str]

    class name(DataProperty, FunctionalProperty):
        domain = [Workflow]
        range = [str]

    class KMObservation(Thing):
        pass
    
    class ExploratoryObservation(KMObservation):
        pass

    class has_exploratory_observations(ObjectProperty):
        domain = [Workflow]
        range = [ExploratoryObservation]

    class exploratory_observation_type(DataProperty, FunctionalProperty):
        domain = [ExploratoryObservation]
        range = [str]



    class DataRepresentationObservation(KMObservation):
        pass

    class has_data_representation_observations(ObjectProperty):
        domain = [Workflow]
        range = [DataRepresentationObservation]

    class data_representation_observation_type(DataProperty, FunctionalProperty):
        domain = [DataRepresentationObservation]
        range = [str]

    class ModellingChoiceObservation(KMObservation):
        pass

    class has_modeling_choice_observations(ObjectProperty):
        domain = [Workflow]
        range = [ModellingChoiceObservation]

    class modelling_choice_observation_type(DataProperty):
        domain = [ModellingChoiceObservation]
        range = [str]

    class ModelSelectionObservation(Thing):
        pass
    
    class has_model_selection_observations(ObjectProperty):
        domain = [Workflow]
        range = [ModelSelectionObservation]

    class model_selection_observation_type(DataProperty, FunctionalProperty):
        domain = [ModelSelectionObservation]
        range = [str]

    class depends_on(ObjectProperty):
        domain = [Workflow]
        range = [KnowledgeExtractionExperimentationWorkflow]

    class ExperimentalObservation(Thing):
        pass

    class has_experimental_observations(ObjectProperty):
        domain = [Workflow]
        range = [ExperimentalObservation]
    
    class experimental_observation_type(DataProperty, FunctionalProperty):
        domain = [ExperimentalObservation]
        range = [str]

    class PerformanceMeasure(Thing):
        pass

    class description(DataProperty):
        range = [str]


    class business_performance_measure(ObjectProperty):
        domain = [KnowledgeApplicationWorkflow]
        range = [PerformanceMeasure]

    class experiment_performance_measure(ObjectProperty):
        domain = [KnowledgeExtractionExperimentationWorkflow]
        range = [PerformanceMeasure]

    class finding(DataProperty, FunctionalProperty):
        Domain =[KMObservation]
        range = [str]

    class finding_sequence(DataProperty, FunctionalProperty):
        Domain =[KMObservation]   
        range = [int]