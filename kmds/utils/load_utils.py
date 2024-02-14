from kmds.ontology.kmds_ontology import *
from owlready2.namespace import Ontology
from typing import List
from pandas import DataFrame
from kmds.utils.path_utils import get_kb_file_path



def get_workflow(onto: Ontology) -> Workflow:
    """Given an ontology, return the workflow instance

    Args:
        onto (Ontology): The ontology from which the workflow instance must be loaded

    Returns:
        Workflow: The workflow in this ontology
    """
    the_workflow_instance = None
    
    with onto:
        workflow_instances = Workflow.instances()
        if workflow_instances is None:
            print("No workflow available")

        else:
            if len(workflow_instances) > 1:
                print("There was more than one workflow, returning the first")
            
            the_workflow_instance = workflow_instances[0]

    return the_workflow_instance


def load_kb(kb_name: str) -> Ontology:
    """ Load knowledge base from data dir. This is a method to be used by other convinience
    methods to load the sets of observations. Not meant to be used directly in a notebookx

    Args:
        kb_name (str): the knowledge base to load

        Returns:
            Ontology: Returns a previously created knowledge base
    """
    try:
        onto: Ontology = get_ontology(get_kb_file_path(kb_name)).load()
        set_ontology(onto)
    except OSError as e:
        print("Error opening KB, check if KB exists and permissions are right")

    return onto


def load_exp_observations(kb_name: str) -> List[ExploratoryObservation]:
    """ Given a Knowledge Base, load the exploratory observations

    Args:
        kb_name (str): the knowledge base from which the exploratory observations are loaded

    Returns:
        List[ExploratoryObservation]: List of exploratory observations
    """

    onto: Ontology = load_kb(kb_name)
    the_workflow: Workflow = get_workflow(onto)
    exp_obs: List[ExploratoryObservation] = the_workflow.has_exploratory_observations
    records = []

    for o in exp_obs:
        a_row = {}
        a_row["obs_type"] = o.exploratory_observation_type
        a_row["finding"] = o.finding
        a_row["finding_seq"] = o.finding_sequence
        records.append(a_row)

    return DataFrame(records)


def load_data_rep_observations(kb_name: str) -> List[DataRepresentationObservation]:
    """ Given a Knowledge Base, load the data representation observations

    Args:
        kb_name (str): the knowledge base from which the data representation observations are loaded

    Returns:
        List[ExploratoryObservation]: List of data representation observations
    """

    onto: Ontology = load_kb(kb_name)
    the_workflow: Workflow = get_workflow(onto)
    dr_obs: List[DataRepresentationObservation] = the_workflow.has_data_representation_observations
    records = []

    for o in dr_obs:
        a_row = {}
        a_row["obs_type"] = o.data_representation_observation_type
        a_row["finding"] = o.finding
        a_row["finding_seq"] = o.finding_sequence
        records.append(a_row)

    return DataFrame(records)

def load_modelling_choice_observations(kb_name: str) -> List[ModellingChoiceObservation]:
    """ Given a Knowledge Base, load the data representation observations

    Args:
        kb_name (str): the knowledge base from which the data representation observations are loaded

    Returns:
        List[ExploratoryObservation]: List of data representation observations
    """

    onto: Ontology = load_kb(kb_name)
    the_workflow: Workflow = get_workflow(onto)
    mc_obs: List[ModellingChoiceObservation] = the_workflow.has_modeling_choice_observations
    records = []

    for o in mc_obs:
        a_row = {}
        a_row["obs_type"] = o.modelling_choice_observation_type
        a_row["finding"] = o.finding
        a_row["finding_seq"] = o.finding_sequence
        records.append(a_row)

    return DataFrame(records)
