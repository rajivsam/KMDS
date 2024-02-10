from ontology.kmds_ontology import *
from owlready2.namespace import Ontology
from typing import List
from pandas import DataFrame
from utils.path_utils import get_kb_file_path

def get_workflow(onto: Ontology) ->Workflow:
    """Given an ontology, return the workflow instance

    Args:
        onto (Ontology): The ontology from which the workflow instance must be loaded

    Returns:
        Workflow: The workflow in this ontology
    """

    ind_instances = onto.individuals()
    the_workflow_instance = None

    for inst in ind_instances:
        is_workflow_instance = isinstance(inst, KnowledgeApplicationWorkflow) | isinstance(inst, KnowledgeExtractionExperimentationWorkflow)
        if is_workflow_instance:
            the_workflow_instance = inst
            break

    
    return the_workflow_instance

def load_kb(kb_name: str) ->Ontology:
    """ Load knowledge base from data dir

    Args:
        kb_name (str): the knowledge base to load

        Returns:
            Ontology: Returns a previously created knowledge base
    """
    try:
        onto : Ontology = get_ontology(get_kb_file_path(kb_name)).load()
    except OSError as e:
        print("Error opening KB, check if KB exists and permissions are right")


    return onto

def load_exp_observations(kb_name: str) ->List[ExploratoryObservation]:

    onto : Ontology = load_kb(kb_name)
    the_workflow : Workflow = get_workflow(onto)
    exp_obs : List[ExploratoryObservation] = the_workflow.has_exploratory_observations
    records = []

    for o in exp_obs:
        a_row = {}
        a_row["obs_type"] = o.exploratory_observation_type
        a_row["finding"] = o.finding
        a_row["finding_seq"] = o.finding_sequence
        records.append(a_row)

    
    return DataFrame(records)