from typing import Dict, Any
from cloud_readers.cloud_data_reader import CloudDataReader
from pandas import DataFrame
import logging
from minio import Minio
import pandas as pd
from io import StringIO
from boxsdk import OAuth2, Client

REQUIRED_INFO = ["CLIENT_ID", "CLIENT_SECRET", "ACCESS_TOKEN"]

class BoxReader(CloudDataReader):


    def __init__(self, conn: Dict[str, Any]) -> None:
        """ This is the class that abstracts the functionality to read from a dropbox collection. To use this reader, create a yaml file (see the repo for an example) with the required entries (see REQUIRED_INFO) and then call the read method with the file identifier of the data file you want to read. Please see the box reader example in the examples directory for details. This file identifier hanlde is a box specific quirk. You can find it by inspecting the file when you log into box. To do: I will subsequently find a way to get the file id from the name. Sorry for the incovinience.

        Args:
            conn (Dict[str, Any]): The information needed to connect to your box account. Create a yaml file with the required entries and then use the config file reader utility to convert to a python dict. Please see the Box reader example for details of how to use this
        """
        super().__init__(conn)
        return

    
    def read_data(self, file_id:str) -> DataFrame:
        """ Use this method to read the data file as a pandas data frame from the source box account. You will need to know the file identifier of the resource within Box (this is a box quirk) to use this method

        Args:
            file_id (str): The file identifier of the data file in your box account. You can find this from the address bar on your browser when you browse the file on your box account

        Returns:
            DataFrame: _description_
        """
        if self._cfg is None:
            logging.error("Initialize the reader with a connection configuration and try again")
        for req_key in REQUIRED_INFO:
            if not req_key in self._cfg:
                logging.error("{required_key} is not in supplied\
                             connection configuration, please add\
                             this and try connectiong again".format(required_key=req_key))
        
        CLIENT_ID = self._cfg["CLIENT_ID"]
        CLIENT_SECRET = self._cfg["CLIENT_SECRET"]
        ACCESS_TOKEN = self._cfg["ACCESS_TOKEN"]
        df : DataFrame = None
        try:
            auth = OAuth2(client_id = CLIENT_ID,
                          client_secret = CLIENT_SECRET,
                          access_token = ACCESS_TOKEN)
            client = Client(auth)
            file_content = client.file(file_id).content()
            s = str(file_content,'utf-8')
            data = StringIO(s)
            df = pd.read_csv(data)
        except :
            msg = "Check your connection parameters, especially the access token. There is a problem connecting. Also verify that the file identifier for the object you want to retrive. You will need to log into Box to verify and obtain this information."

            logging.error(msg)
        
        return df
            
