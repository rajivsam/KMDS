import yaml
from typing import Dict, Any
from pathlib import Path
import os

def get_config(config_file_name: str) -> Dict[Any, Any]:
    """ Load the config file from the config directory, use the yaml library to return a dictionary configuration

    Args:
        config_file_name (str): the name of the config file

    Returns:
        Dict[Any, Any]: The config file as a python dictionary - has keys for properties and values for corresponding settings
    """
    assert config_file_name is not None
    fp =  "kmds/config/"+ config_file_name

    with open(fp) as fp:
        cfg = yaml.safe_load(fp)
    return cfg
