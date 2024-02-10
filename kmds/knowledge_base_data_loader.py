from ontology.kmds_ontology import *
from typing import List
from utils.path_utils import get_ontology_path, get_kb_file_path
from owlready2.namespace import Ontology
from pathlib import Path
import types
from pandas import DataFrame

class KnowledgeBaseDataLoader:

    def __init__(self, kb_name: str) -> None:
        """ Instantiation loads the knowledge base from the data directory

        Args:
            kb_name (str): the knowledge base to load
        """
        self._onto :Ontology = self.load_kb(kb_name)
        #the_workflow_instance = list(self._onto.individuals())[0]
        the_workflow_instance = self.get_workflow_instance()
        
        if isinstance(the_workflow_instance, KnowledgeApplicationWorkflow):
            self._aw : KnowledgeApplicationWorkflow = the_workflow_instance
        else:
            self._aw :KnowledgeExtractionExperimentationWorkflow = the_workflow_instance

        return
    
    def get_workflow_instance(self) -> Workflow:
        """ Return the workflow instance from the loaded ontology

        Returns:
            Workflow: the workflow instance in the loaded ontology
        """

        ind_instances = self._onto.individuals()
        the_workflow_instance = None

        for inst in ind_instances:
            is_workflow_instance = isinstance(inst, KnowledgeApplicationWorkflow) | isinstance(inst, KnowledgeExtractionExperimentationWorkflow)
            if is_workflow_instance:
                the_workflow_instance = inst
                break

        return the_workflow_instance


    def load_kb(self, kb_name: str) ->Ontology:
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
    
    

    def load_exploratory_obs(self) -> DataFrame:
        exp_obs : List[ExploratoryObservation] = self._aw.has_exploratory_observations
        records = []

        for o in exp_obs:
            a_row = {}
            a_row["obs_type"] = o.exploratory_observation_type
            a_row["finding"] = o.finding
            a_row["finding_seq"] = o.finding_sequence
            records.append(a_row)

        return DataFrame(records)