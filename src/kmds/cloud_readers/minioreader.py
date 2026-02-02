from typing import Dict, Any
from cloud_readers.cloud_data_reader import CloudDataReader
from pandas import DataFrame
import logging
from minio import Minio
import pandas as pd
from io import StringIO

REQUIRED_INFO = ["HOST_URL", "ACCESS_KEY", "SECRET_KEY"]

class MinioReader(CloudDataReader):

    def __init__(self, conn: Dict[str, Any]) -> None:
        """ This is the class to read data from a Minio cloud storage bucket. 

        Args:
            conn (Dict[str, Any]): This is the connection information to connect and read data from the Minio storage location. Please see the example notebook provided for details that are needed. The information in the REQUIRED_INFO list must be provided. There is a utility to convert a yaml file containing this information to python dictionary. Please see the example notebook for details.
        """
        super().__init__(conn)
        return
    
    def read_data(self, bucket_name: str, object_name: str) -> DataFrame:
        """ Use this method to read a object (data file) from the bucket (bucket name)

        Args:
            bucket_name (str): the bucket name containing the datafile
            object_name (str): data file with bucket that must be read

        Returns:
            DataFrame: A pandas datafreame wrapping the data file
        """
        if self._cfg is None:
            logging.error("Initialize the reader with a connection configuration and try again")
        for req_key in REQUIRED_INFO:
            if not req_key in self._cfg:
                logging.error("{required_key} is not in supplied\
                             connection configuration, please add\
                             this and try connectiong again".format(required_key=req_key))
        
        HOST_URL = self._cfg["HOST_URL"]
        ACCESS_KEY = self._cfg["ACCESS_KEY"]
        SECRET_KEY = self._cfg["SECRET_KEY"]
        df : DataFrame = None

        try:
            client = Minio(endpoint=HOST_URL, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=True)
            obj = client.get_object(bucket_name, object_name)
            data = obj.data
            s = str(data,'utf-8')
            data = StringIO(s)
            df = pd.read_csv(data)
        except :
            msg = "Check connection parameters and if the object to be read exists in the remote bucket. There was a problem getting the remote object"
            logging.error(msg)
        
        return df
        
            
        


        
