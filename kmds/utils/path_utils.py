from pathlib import Path
import os

def get_ontology_path() ->Path:
    return os.path.join(Path(__file__).absolute().parent.parent, "ontology/kmds_ontology.xml")

def get_kb_file_path(file_name: str) ->Path:
    kb_segment = "data/" + file_name + ".xml"
    return os.path.join(Path(__file__).absolute().parent.parent.parent, kb_segment) 