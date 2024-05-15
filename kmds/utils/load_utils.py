from kmds.ontology.kmds_ontology import *
from owlready2.namespace import Ontology
from typing import List

from pandas import DataFrame
import logging


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
                logging.info(
                    "There was more than one workflow, using the first one")

            the_workflow_instance = workflow_instances[0]

    return the_workflow_instance


def load_kb(kb_location: str) -> Ontology:
    """ Load knowledge base. The user can verify the knowledge base path with check_valid_path() in
    path utils, the knowledge base can be a url, the onus of verifying that that the knowledgebase location is valid is on the caller of the method, this method does not verify the validity

    Args:
        kb_name (str): the knowledge base to load

        Returns:
            Ontology: Returns a previously created knowledge base
    """
    onto: Ontology = None
    try:
        onto = get_ontology(kb_location).load()
        set_ontology(onto)
    except Exception as e:
        logging.error(
            "Error opening KB, check if KB exists and permissions are right")
    if onto is None:
        logging.error("Could not load Ontology, check the file and try again.")

    return onto


def load_exp_observations(onto: Ontology) -> List[ExploratoryObservation]:
    """ Return the exploratory data analysis observations from the ontology

    Args:
        onto (Ontology): The ontology from which the EDA observations are to be returned

    Returns:
        List[ExploratoryObservation]: List of EDA observations in the ontology
    """

    the_workflow: Workflow = get_workflow(onto)
    exp_obs: List[ExploratoryObservation] = the_workflow.has_exploratory_observations
    records = []

    for o in exp_obs:
        a_row = {}
        a_row["obs_type"] = o.exploratory_observation_type
        a_row["finding"] = o.finding
        a_row["finding_seq"] = o.finding_sequence
        intent_present = o.intent is not None
        if intent_present:
            a_row["intent"] = o.intent
        records.append(a_row)
    df = DataFrame(records)
    
    if df.shape[0] > 0:
        if len(df.columns.to_list()) == 4:
            ord_col = ["obs_type", "intent", "finding", "finding_seq"]
        else:
            ord_col = ["obs_type", "finding", "finding_seq"]
        df = df[ord_col]


    return df


def load_data_rep_observations(onto: Ontology) -> List[DataRepresentationObservation]:
    """ Load the data representation observations from the provided ontology

    Args:
        onto (Ontology): The ontology containing the data representation observations

    Returns:
        List[DataRepresentationObservation]: The list of data representation observations
    """

    the_workflow: Workflow = get_workflow(onto)
    dr_obs: List[DataRepresentationObservation] = the_workflow.has_data_representation_observations
    records = []

    for o in dr_obs:
        a_row = {}
        a_row["obs_type"] = o.data_representation_observation_type
        a_row["finding"] = o.finding
        a_row["finding_seq"] = o.finding_sequence

        intent_present = o.intent is not None
        if intent_present:
            a_row["intent"] = o.intent
        records.append(a_row)
    
    df = format_records(records=records)

    return df


def load_modelling_choice_observations(onto: Ontology) -> List[ModellingChoiceObservation]:
    """ Load the modelling choice observations from the ontology

    Args:
        onto (Ontology): The ontology containing modelling choice observations

    Returns:
        List[ModellingChoiceObservation]: The list of modelling choice observations in the ontology
    """

    the_workflow: Workflow = get_workflow(onto)
    mc_obs: List[ModellingChoiceObservation] = the_workflow.has_modeling_choice_observations
    records = []

    for o in mc_obs:
        a_row = {}
        a_row["obs_type"] = o.modelling_choice_observation_type
        a_row["finding"] = o.finding
        a_row["finding_seq"] = o.finding_sequence

        intent_present = o.intent is not None
        if intent_present:
            a_row["intent"] = o.intent
        records.append(a_row)
    
    df = format_records(records=records)


    return df


def load_model_selection_observations(onto: Ontology) -> List[ModelSelectionObservation]:
    """ Load the model selection observations from the ontology

    Args:
        onto (Ontology): The ontology containing the model selection observations

    Returns:
        List[ModelSelectionObservation]: The list of model selection observations
    """

    the_workflow: Workflow = get_workflow(onto)
    mc_obs: List[ModelSelectionObservation] = the_workflow.has_model_selection_observations
    records = []

    for o in mc_obs:
        a_row = {}
        a_row["obs_type"] = o.model_selection_observation_type
        a_row["finding"] = o.finding
        a_row["finding_seq"] = o.finding_sequence

        intent_present = o.intent is not None
        if intent_present:
            a_row["intent"] = o.intent
        records.append(a_row)
    df = format_records(records=records)


    return df

def format_records(records: List[KMObservation] ) ->DataFrame:
    """ Format a list of observations into a dataframe for display

    Args:
        records (List[KMObservation]):  List of observations

    Returns:
        DataFrame: Dataframe containing the records
    """
    df = DataFrame(records)
    if df.shape[0] > 0:
        if len(df.columns.to_list()) == 4:
            ord_col = ["obs_type", "intent", "finding", "finding_seq"]
        else:
            ord_col = ["obs_type", "finding", "finding_seq"]
        df = df[ord_col]

        

    return df
