from typing import Dict, Any
from pandas import DataFrame
from abc import ABC, abstractmethod

class CloudDataWriter(ABC):
   def __init__(self, conn:Dict[str, Any]) -> None: 
       """ Abstract base class encapsulating data writes to a cloud endpoint

       Args:
           conn (Dict[str, Any]): Connection information to connect to the endpoint
       """
       self._cfg = conn
       return
