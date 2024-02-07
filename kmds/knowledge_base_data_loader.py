from ontology.kmds_ontology import *
from typing import List
from utils.path_utils import get_ontology_path, get_kb_file_path
from owlready2.namespace import Ontology
from pathlib import Path
import types
from pandas import DataFrame

class KnowledgeBaseDataLoader:

    def __init__(self, kb_name: str) -> None:
        self._onto :Ontology = self.load_kb(kb_name)
        the_workflow_instance = self._onto.KnowledgeApplicationWorkflow.instances()[0]
        if isinstance(the_workflow_instance, KnowledgeApplicationWorkflow):
            self._aw : KnowledgeApplicationWorkflow = the_workflow_instance
        else:
            self._aw :KnowledgeExtractionExperimentationWorkflow = the_workflow_instance

        return
    
    def load_kb(self, kb_name) -> Ontology:
        try:
            fp: Path = get_kb_file_path(kb_name)
            onto: Ontology = get_ontology(fp).load()
        except OSError as error:
            print("eror loading knowledge base: " + error)
            print("cannot load knowledge base - check file name and permissions")
        
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