from pathlib import Path
import os
from importlib_resources import files

def get_ontology_path() ->Path:
    """ Return the ontology file path as a Path

    Returns:
        Path: the path to the ontology file 
    """
    file_path = str(files('kmds.ontology').joinpath('kmds_ontology.xml'))
    #p = os.path.join(Path(__file__).absolute().parent.parent, "ontology/kmds_ontology.xml")
    
    return file_path

def get_kb_file_path(file_name: str) ->Path:
    """ Given a file name for a knowledge base, return the path to it as a Path

    Args:
        file_name (str): the filename of the knowledge base

    Returns:
        Path: the path corresponding to the provided file name
    """



    file_path =  str(files('kmds.examples').joinpath(file_name))
    return file_path

def get_kb_dir() ->Path:
    return str(files('kmds.examples'))



