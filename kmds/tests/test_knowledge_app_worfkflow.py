import pytest
from tagging.tag_types import *
from ontology.kmds_ontology import *
from typing import List
from utils.path_utils import *
from knowledge_base_data_loader import KnowledgeBaseDataLoader
from utils.observation_sequence_generator import ObservationSequence

NUM_OBSERVATIONS = 5

def generate_exploratory_observations() -> List[ExploratoryObservation]:
    """ Generates the exploratory observations for the test cas

    Returns:
        List[ExploratoryObservation]: list of exporatory observations created for testing
    """
    exp_obs : List[ExploratoryObservation] = []
    obs_type = [ ExploratoryTags.RELEVANCE_OBSERVATION.value, ExploratoryTags.DATA_QUALITY_OBSERVATION.value]
    sg = ObservationSequence()
    for i in range(NUM_OBSERVATIONS):
        tag_index = i % 2
        seq = i+1
        e = ExploratoryObservation()
        e.finding = "Exploratory Observation - " + str(sg.next_obs_number())
        e.finding_sequence = seq
        e.exploratory_observation_type = obs_type[tag_index]

        exp_obs.append(e)
    return exp_obs

def generate_data_representation_observations() -> List[DataRepresentationObservation]:
    """ Generates the data representation observations for testing

    Returns:
        List[DataRepresentationObservation]: list of data representation observations for testing
    """
    data_rep_obs : List[DataRepresentationObservation] = []
    obs_type = [ DataRepresentationTags.FEATURE_ENGG_OBSERVATION.value, DataRepresentationTags.DATA_TRANSFORMATION_OBSERVATION.value]
    sg = ObservationSequence()
    for i in range(NUM_OBSERVATIONS):
        tag_index = i % 2
        seq = i+1
        e = DataRepresentationObservation()
        e.finding = "Data Representation Observation - " + str(sg.next_obs_number())
        e.finding_sequence = seq
        e.data_representation_observation_type = obs_type[tag_index]

        data_rep_obs.append(e)
    return data_rep_obs

def generate_experimental_observations() -> List[ExperimentalObservation]:
    """ Generate experimental observations for testing

    Returns:
        List[ExperimentalObservation]: List of experimental observations
    """
    exp_obs : List[ExperimentalObservation] = []
    obs_type = [ ExperimentationTags.HYPOTHESIS_STATEMENT, ExperimentationTags.EXPERIMENTAL_OBSERVATION.value, ExperimentationTags.EXPERIMENTAL_CONJECTURE, ExperimentationTags.RESULT_SUMMARY]
    sg = ObservationSequence()
    for i in range(NUM_OBSERVATIONS):
        tag_index = i % len(obs_type)
        seq = i+1
        e = ExperimentalObservation()
        e.finding = "Experimental Observation - " + str(sg.next_obs_number())
        e.finding_sequence = seq
        e.experimental_observation_type = obs_type[tag_index]

        exp_obs.append(e)
    return exp_obs
    

def test_knowledge_application_workflow():
    """ Test the knowledge application workflow 
    """
    kaw: KnowledgeApplicationWorkflow = KnowledgeApplicationWorkflow("test application workflow")
    assert kaw is not None

    exp_obs = generate_exploratory_observations()

    kaw.has_exploratory_observations = exp_obs
    num_obs_exp = len(kaw.has_exploratory_observations)
    
    assert num_obs_exp == 5

    data_rep_obs = generate_data_representation_observations()
    kaw.has_data_representation_observations = data_rep_obs

    num_obs_data_rep = len(kaw.has_data_representation_observations)

    assert num_obs_data_rep == 5
    onto = get_ontology(get_ontology_path()).load()
    onto.save(file=get_kb_file_path(file_name="test_kb_app_workflow"), format="rdfxml")

    return

def test_knowledge_extraction_experiment_workflow():
    """ Test the knowledge extraction experiment workflow.
    """
    keew: KnowledgeExtractionExperimentationWorkflow = KnowledgeExtractionExperimentationWorkflow("test experiment workflow")
    assert keew is not None

    exp_obs = generate_exploratory_observations()

    keew.has_exploratory_observations = exp_obs
    num_obs_exp = len(keew.has_exploratory_observations)
    
    assert num_obs_exp == 5

    data_rep_obs = generate_data_representation_observations()
    keew.has_data_representation_observations = data_rep_obs

    num_obs_data_rep = len(keew.has_data_representation_observations)

    assert num_obs_data_rep == 5
    onto = get_ontology(get_ontology_path()).load()
    onto.save(file=get_kb_file_path(file_name="test_kb_exp_workflow"), format="rdfxml")

    return

def test_load_knowledge_base_application_workflow():
    """ Test the load application knowledge base workflow.
    """
    kb_dl = KnowledgeBaseDataLoader("test_kb_app_workflow")
    df = kb_dl.load_exploratory_obs()
    assert df.shape[0] == 5

    return

def test_load_knowledge_base_exp_workflow():
    """ Test the load experimental knowledge base workflow
    """
    kb_dl = KnowledgeBaseDataLoader("test_kb_exp_workflow")
    df = kb_dl.load_exploratory_obs()
    assert df.shape[0] == 5

    return





if __name__ == '__main__':
    test_knowledge_application_workflow()
    test_knowledge_extraction_experiment_workflow()
    test_load_knowledge_base_application_workflow()
    test_load_knowledge_base_exp_workflow()

