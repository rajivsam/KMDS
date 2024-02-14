import pytest
from kmds.tagging.tag_types import *
from kmds.ontology.kmds_ontology import *
from typing import List
from kmds.utils.path_utils import *
from owlready2 import *
from kmds.utils.load_utils import *

NUM_OBSERVATIONS = 5

 


def generate_exploratory_observations() -> List[ExploratoryObservation]:
    """ Generates the exploratory observations for the test cas

    Returns:
        List[ExploratoryObservation]: list of exporatory observations created for testing
    """
    exp_obs : List[ExploratoryObservation] = []
    obs_type = [ ExploratoryTags.RELEVANCE_OBSERVATION.value, ExploratoryTags.DATA_QUALITY_OBSERVATION.value]
  

    for i in range(NUM_OBSERVATIONS):
        tag_index = i % 2
        seq = i+1
        e = ExploratoryObservation()
        e.finding = "Exploratory Observation - " + str(seq)
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

    for i in range(NUM_OBSERVATIONS):
        tag_index = i % 2
        seq = i+1
        e = DataRepresentationObservation()
        e.finding = "Data Representation Observation - " + str(seq)
        e.finding_sequence = seq
        e.data_representation_observation_type = obs_type[tag_index]

        data_rep_obs.append(e)
    return data_rep_obs

def generate_modelling_choice_observations() -> List[ModellingChoiceObservation]:
    """ Generates the modelling choice observations for testing

    Returns:
        List[ModellingChoice]: list of modelling choice observations
    """
    mc_obs : List[ModellingChoiceObservation] = []
    obs_type = [ ModellingChoiceTags.MODELLING_ASSUMPTION_OBSERVATION.value, ModellingChoiceTags.MODELLING_CHOICE_OBSERVATION.value]

    for i in range(NUM_OBSERVATIONS):
        tag_index = i % 2
        seq = i+1
        e = ModellingChoiceObservation()
        e.finding = "Modelling Choice Observation - " + str(seq)
        e.finding_sequence = seq
        e.modelling_choice_observation_type = obs_type[tag_index]

        mc_obs.append(e)
    return mc_obs

def generate_model_selection_observations() -> List[ModelSelectionObservation]:
    """ Generates the data representation observations for testing

    Returns:
        List[ModelSelectionObservation]: list of model selection observations for testing
    """
    ms_obs : List[ModelSelectionObservation] = []
    obs_type = [ ModelSelectionTags.MODEL_SELECTION_OBSERVATION.value, ModelSelectionTags.MODEL_SELECTION_RESULT_SUMMARY.value, ModelSelectionTags.MODEL_SELECTION_SETUP_DESCRIPTION.value, ModelSelectionTags.MODEL_SELECTION_STATEMENT.value]

    for i in range(NUM_OBSERVATIONS):
        tag_index = i % len(obs_type)
        seq = i+1
        e = ModellingChoiceObservation()
        e.finding = "Modelling Choice Observation - " + str(seq)
        e.finding_sequence = seq
        e.modelling_choice_observation_type = obs_type[tag_index]

        ms_obs.append(e)
    return ms_obs


    

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
    
    mc_obs = generate_modelling_choice_observations()
    kaw.has_modeling_choice_observations = mc_obs

    num_obs_mc = len(kaw.has_modeling_choice_observations)

    assert num_obs_mc == 5
    ms_obs = generate_model_selection_observations()
    kaw.has_model_selection_observations = ms_obs

    num_obs_ms = len(kaw.has_model_selection_observations)

    assert num_obs_ms == 5
    
    onto = get_ontology(get_ontology_path()).load()
    onto.save(file=get_kb_file_path("test_kb_app_workflow"), format="rdfxml")
    #onto.destroy()

def test_knowledge_extraction_experiment_workflow():
    """ Test the knowledge extraction experiment workflow.
    """

    #onto = get_ontology(get_ontology_path()).load()
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

    mc_obs = generate_modelling_choice_observations()
    keew.has_modeling_choice_observations = mc_obs

    num_obs_mc = len(keew.has_modeling_choice_observations)

    assert num_obs_mc == 5
    ms_obs = generate_model_selection_observations()
    keew.has_model_selection_observations = ms_obs

    num_obs_ms = len(keew.has_model_selection_observations)

    assert num_obs_ms == 5

    onto = get_ontology(get_ontology_path()).load()
    onto.save(file=get_kb_file_path("test_kb_exp_workflow"), format="rdfxml")

    return


def test_load_knowledge_base_application_workflow():
    """ Test the load application knowledge base workflow.
    """

    dfe = load_exp_observations("test_kb_app_workflow")
    dfd = load_data_rep_observations("test_kb_app_workflow")
    assert dfe.shape[0] == 5
    assert dfd.shape[0] == 5

    return

def test_load_knowledge_base_exp_workflow():
    """ Test the load experimental knowledge base workflow
    """
    dfe = load_exp_observations("test_kb_exp_workflow")
    dfd = load_data_rep_observations("test_kb_exp_workflow")
    dfmc = load_modelling_choice_observations("test_kb_exp_workflow")
    dfms = load_model_selection_observations("test_kb_exp_workflow")
    assert dfe.shape[0] == 5
    assert dfd.shape[0] == 5
    assert dfmc.shape[0] == 5
    assert dfms.shape[0] == 5

    return





if __name__ == '__main__':
    test_knowledge_application_workflow()
    test_knowledge_extraction_experiment_workflow()
    test_load_knowledge_base_application_workflow()
    test_load_knowledge_base_exp_workflow()

