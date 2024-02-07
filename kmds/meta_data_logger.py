from ontology.kmds_ontology import *
from typing import List
from utils.path_utils import get_ontology_path, get_kb_file_path


class MetaDataLogger:

    def __init__(self, pipeline_name: str, piplline_type: PipelineType) -> None:
        """ Class abstraction to log observations to the knowledge base

        Args:
            pipeline_name (str): the pipeline name to log to
            piplline_type (PipelineType): the type of pipeline - knowledge application or knowledge extraction experiment
        """
        self._pipeline_name: str = pipeline_name
        self._pipeline_type: str = piplline_type

        if self._pipeline_type == PipelineType.KNOWLEDGE_APPLICATION_WORKFLOW:
            self._aw : KnowledgeApplicationWorkflow = KnowledgeApplicationWorkflow(self._pipeline_name)
        else:
            self._aw : KnowledgeExtractionExperimentationWorkflow =  KnowledgeExtractionExperimentationWorkflow(
            self._pipeline_name)
        print("workflow type is : " + str(type(self._aw)))

        return
    
    def save_knowledge_base(self, file_name: str) -> None:
        """ Save the knowledge base to the supplied file name

        Args:
            file_name (str): The file name to save the knowledge base to
        """
        assert file_name is not None
        onto = get_ontology(get_ontology_path()).load()
        onto.save(file=get_kb_file_path(file_name=file_name), format="rdfxml")

        return


    def log_exploratory_observations(self, exploratory_findings: List[ExploratoryObservation]) -> None:
        """ Log the list of exploratory observations to the ontology

        Args:
            exploratory_findings (List[ExploratoryObservation]): List of exploratory observations
        """
        self._aw.has_exploratory_observations = exploratory_findings

        return

    def log_data_representation_observations(self, data_representation_obs: List[DataRepresentationObservation]) -> None:
        """ Log the list of data representation observations to the ontology

        Args:
            data_representation_obs (List[DataRepresentationObservation]): List of data representation observations received
        """
        self._aw.has_data_representation_observations = data_representation_obs


        return

    def log_modelling_choice_observations(self, modelling_choice_obs: List[ModellingChoiceObservation]) -> None:
        """ Log modelling choice observations to the ontology

        Args:
            modelling_choice_obs (List[ModellingChoiceObservation]): list of modelling choice observations
        """

        for obs in modelling_choice_obs:
            obs.is_modelling_choice_observation_of_type.append(obs.obs_type)
            obs.log_modelling_choice_fact(obs.description)
            obs.log_modelling_choice_fact_sequence(obs.sequence)
            self._aw.has_modeling_choice_observations.append(obs)

        return
    
    def log_model_selection_observations(self, model_selection_obs: List[ModellingChoiceObservation]) -> None:
        """ Log model selection observations to the ontology

        Args:
            model_selection_obs (List[ModellingChoiceObservation]): list of model selection observations
        """

        for obs in model_selection_obs:
            obs.is_model_selection_observation_of_type.append(obs.obs_type)
            obs.log_model_selection_fact(obs.description)
            obs.log_model_selection_fact_sequence(obs.sequence)
            self._aw.has_model_selection_observations.append(obs)

        return
