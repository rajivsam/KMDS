import yaml
from typing import Dict, Any
from pathlib import Path
import os

def get_config(config_file_name: str) -> Dict[Any, Any]:
    assert config_file_name is not None
    fp =  "kmds/config/"+ config_file_name

    with open(fp) as fp:
        cfg = yaml.safe_load(fp)
    return cfg
