from typing import Dict, Any
from pandas import DataFrame
from abc import ABC, abstractmethod

class CloudDataReader(ABC):

   def __init__(self, conn:Dict[str, Any]) -> None: 
       """ This is the abstract base class for the cloud data readers.

       Args:
           conn (Dict[str, Any]):  A dictionary containing the connection parameters to connect to the data source (for example, an S3 bucket or a box account.)
       """
       self._cfg = conn
       return
    

