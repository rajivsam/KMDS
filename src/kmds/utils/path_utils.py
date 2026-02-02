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

def check_valid_path(file_path: Path) -> bool:
    """ Check if a file exists at the provided path

    Args:
        file_path (Path): The path to a file

    Returns:
        bool: True if the file exists, else False
    """
    if file_path.is_file():
        return True
    else:
        return False
    
def get_package_kb_path(kb_name: str) ->str:
    """ Return path string to a package knowledge base

    Args:
        kb_name (str): The knowledge base name

    Returns:
        str: The path (as a string) to the package knowledge base
    """
    file_path =  str(files('kmds.examples').joinpath(kb_name))
    return file_path

    




