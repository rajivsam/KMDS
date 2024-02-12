from pathlib import Path
import os

def get_ontology_path() ->Path:
    """ Return the ontology file path as a Path

    Returns:
        Path: the path to the ontology file 
    """
    p = os.path.join(Path(__file__).absolute().parent.parent, "ontology/kmds_ontology.xml")
    file_path =  p
    return file_path

def get_kb_file_path(file_name: str) ->Path:
    """ Given a file name for a knowledge base, return the path to it as a Path

    Args:
        file_name (str): the filename of the knowledge base

    Returns:
        Path: the path corresponding to the provided file name
    """
    kb_segment = "data/" + file_name + ".xml"
    p = os.path.join(Path(__file__).absolute().parent.parent.parent, kb_segment)
    file_path =  p
    return file_path

def get_kb_dir() ->Path:
    kb_segment = "data/" 
    return os.path.join(Path(__file__).absolute().parent.parent.parent, kb_segment)



