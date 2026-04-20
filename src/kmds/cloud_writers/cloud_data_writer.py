from typing import Dict, Any

class CloudDataWriter:
   def __init__(self, conn:Dict[str, Any]) -> None: 
       """ Abstract base class encapsulating data writes to a cloud endpoint

       Args:
           conn (Dict[str, Any]): Connection information to connect to the endpoint
       """
       self._cfg = conn
       return
