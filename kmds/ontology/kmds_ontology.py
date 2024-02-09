from owlready2 import *
from typing import List
from enum import Enum
from tagging import *
import os
from utils.path_utils import get_ontology_path
from pathlib import Path 



class PipelineType(str, Enum):
    """ Enumeration to define the types of workflows that can be created

    Args:
        str (_type_): The enumeration values are strings
        Enum (_type_): The enumeration values are strings
    """
    KNOWLEDGE_APPLICATION_WORKFLOW = "Knowledge Application Workflow"
    KNOWLEDGE_EXTRACTION_EXPERIMENT_WORKFLOW = "Knowledge Extraction Experiment Workflow"



onto = get_ontology(get_ontology_path())

with onto:
    class Workflow(Thing):
        """ Ontology definition for workflow

        Args:
            Thing (_type_): Thing is a base concept from OWL
        """
        pass
    class KnowledgeApplicationWorkflow(Workflow):
        """ knowledge application workflow definition - inherits from workflow

        Args:
            Workflow (_type_): Base workflow classxs
        """

        pass
    
    class KnowledgeExtractionExperimentationWorkflow(Workflow):
        """ knowledge extraction experiment workflow definition - inherits from workflow

        Args:
            Workflow (_type_): Base workflow class
        """

        pass
    
    class description(DataProperty, FunctionalProperty):
        """ Description as property of workflow

        Args:
            DataProperty (_type_): This is a OWLReady2 way to say that this property is of a built in type as opposed to a defined type
            FunctionalProperty (_type_): This is a OWLReady2 way to say that this property is of a built in type as opposed to a defined type
        """
        

        domain = [Workflow]
        range = [str]

    class name(DataProperty, FunctionalProperty):
        """ name as property of workflow

        Args:
            DataProperty (_type_): This is a OWLReady2 way to say that this property is of a built in type as opposed to a defined type
            FunctionalProperty (_type_): This is a OWLReady2 way to say that this property is of a built in type as opposed to a defined type
        """

        domain = [Workflow]
        range = [str]

    class KMObservation(Thing):
        """ Base class for observations, the specific types of observations derive from this class

        Args:
            Thing (_type_): OWL base class for everything
        """
        pass
    
    class ExploratoryObservation(KMObservation):
        """ Class to capture exploratory observations

        Args:
            KMObservation (_type_): the base observation class
        """
        pass

    class has_exploratory_observations(ObjectProperty):
        """ property to capture the exploratory observations of the workflow

        Args:
            ObjectProperty (_type_): captures the exploratory observations of the workflow
        """
        domain = [Workflow]
        range = [ExploratoryObservation]

    class exploratory_observation_type(DataProperty, FunctionalProperty):
        """ property to capture the type of exploratory observation - see tagging types for the options

        Args:
            DataProperty (_type_): OWL2library specific way of defining a property with a built in value
            FunctionalProperty (_type_): OWL2library specific way of defining a property with a built in value
        """
        domain = [ExploratoryObservation]
        range = [str]



    class DataRepresentationObservation(KMObservation):
        """ property to capture the data representation observation

        Args:
            KMObservation (_type_): base class for observations
        """
        pass

    class has_data_representation_observations(ObjectProperty):
        """ Property to capture the data representation observations of a workflow

        Args:
            ObjectProperty (_type_): OWLReady2 specific way of capturing object properties
        """
        domain = [Workflow]
        range = [DataRepresentationObservation]

    class data_representation_observation_type(DataProperty, FunctionalProperty):
        """ Specify the data representation observation type

        Args:
            DataProperty (_type_): OWLReady2 specific way of specifying the data property type
            FunctionalProperty (_type_): OWLReady2 specific way of specifying the data property type
        """
        domain = [DataRepresentationObservation]
        range = [str]

    class ModellingChoiceObservation(KMObservation):
        """ Definition of modelling choice observations

        Args:
            KMObservation (_type_): Base class for observations
        """
        pass

    class has_modeling_choice_observations(ObjectProperty):
        """ Specify that the workflow has modelling choice observations

        Args:
            ObjectProperty (_type_): the OWLReady2 way to specify that these observations are objects
        """
        domain = [Workflow]
        range = [ModellingChoiceObservation]

    class modelling_choice_observation_type(DataProperty):
        """ Specify that the modelling observation type in tagging modelling choice observations - see tagging for the options available

        Args:
            DataProperty (_type_): OWLReady2 specific way of describing properties
        """
        domain = [ModellingChoiceObservation]
        range = [str]

    class ModelSelectionObservation(Thing):
        """ Definition of Model Selection Observations

        Args:
            Thing (_type_): Base class for everything in OWL
        """
        pass
    
    class has_model_selection_observations(ObjectProperty):
        """ Specify that the workflow has model selection observations recorded

        Args:
            ObjectProperty (_type_): OWLReady2 specific way of capturing object properties
        """
        domain = [Workflow]
        range = [ModelSelectionObservation]

    class model_selection_observation_type(DataProperty, FunctionalProperty):
        """ Specify the model selection observation type - see tagging for options

        Args:
            DataProperty (_type_): OWLReady2 specific of specifying properties of builtin type
            FunctionalProperty (_type_): OWLReady2 specific of specifying properties of builtin type
        """
        domain = [ModelSelectionObservation]
        range = [str]

    class depends_on(ObjectProperty):
        """ Property to capture the workflows that a particular workflow is informed by, and, therefore depends on, these workflows must have been run prior to this workflow

        Args:
            ObjectProperty (_type_): OWLReady2 specific way of specifying Object properties, as opposed to built in types
        """
        domain = [Workflow]
        range = [KnowledgeExtractionExperimentationWorkflow]

    class ExperimentalObservation(Thing):
        """ Define experimental observation type

        Args:
            Thing (_type_): OWL base class for everything
        """
        pass

    class has_experimental_observations(ObjectProperty):
        """ Property of the workflow to capture its experimental observations

        Args:
            ObjectProperty (_type_): OWLReady2 specific way of specifying that this property is an object type as opposed to a built in type
        """
        domain = [Workflow]
        range = [ExperimentalObservation]
    
    class experimental_observation_type(DataProperty, FunctionalProperty):
        """ Property to capture the experimental observation type - see tagging for definition

        Args:
            DataProperty (_type_): OWLReady2 specific way of defining built in types as properties
            FunctionalProperty (_type_): OWLReady2 specific way of defining built in types as properties
        """
        domain = [ExperimentalObservation]
        range = [str]

    class PerformanceMeasure(Thing):
        """ Definition of performance measure as a concept

        Args:
            Thing (_type_): OWL base class for everything
        """
        pass

    class description(DataProperty):
        """ description of the workflow

        Args:
            DataProperty (_type_): OWLReady2 specific way of describing built in type properties
        """
        range = [str]


    class business_performance_measure(ObjectProperty):
        """ Capture the business performance measure of the workflow

        Args:
            ObjectProperty (_type_): OWLReady2 specific way of specifying object properties
        """
        domain = [KnowledgeApplicationWorkflow]
        range = [PerformanceMeasure]

    class experiment_performance_measure(ObjectProperty):
        """ Property to capture experiment performance measure

        Args:
            ObjectProperty (_type_): Experiment performance measure as an object property
        """
        domain = [KnowledgeExtractionExperimentationWorkflow]
        range = [PerformanceMeasure]

    class finding(DataProperty, FunctionalProperty):
        """ Speficy the finding property of an observation

        Args:
            DataProperty (_type_): OWLReady 2 specific way to say that the range is a srting
            FunctionalProperty (_type_): OWLReady 2 specific way to say that the domain is an object
        """
        Domain =[KMObservation]
        range = [str]

    class finding_sequence(DataProperty, FunctionalProperty):
        """ Speficy the finding sequence property of an observation

        Args:
            DataProperty (_type_): OWLReady 2 specific way to say that the range is an integer
            FunctionalProperty (_type_): OWLReady 2 specific way to say that the domain is an object
        """
        Domain =[KMObservation]   
        range = [int]