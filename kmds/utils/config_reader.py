import yaml
from typing import Dict, Any
import logging


def get_config(config_file_name: str) -> Dict[Any, Any]:
    """ Load the config file from the config directory, use the yaml library to return a dictionary configuration

    Args:
        config_file_name (str): the name of the config file, this is the absolute path as a string

    Returns:
        Dict[Any, Any]: The config file as a python dictionary - has keys for properties and values for corresponding settings
    """
    assert config_file_name is not None
    
    config_file_name

    with open(config_file_name) as fp:
        try:
            cfg = yaml.safe_load(fp)
        except Exception:
            logging.error("Could not write to file at: " +  config_file_name)
            logging.error("Please verify file exists and valid, then try again!")

    return cfg
