from typing import Dict, Any
from cloud_writers.cloud_data_writer import CloudDataWriter
from pandas import DataFrame
import logging
from minio import Minio


REQUIRED_INFO = ["HOST_URL", "ACCESS_KEY", "SECRET_KEY"]

class MinioWriter(CloudDataWriter):

    def __init__(self, conn: Dict[str, Any]) -> None:
        """ This class abstracts the details of connecting and writing a data file to a Minio (S3) bucket.

        Args:
            conn (Dict[str, Any]): The connection information to connect to the bucket, please see REQUIRED_INFO for the list of parameters that must be provided
        """
        super().__init__(conn)
        return
    
    def write_data(self, bucket_name: str, source_file: str, destination_file: str) -> None:
        """ This method writes the source file argument to the bucket name argument

        Args:
            bucket_name (str): The bucket name to which the source file must be written
            source_file (str): The source file to be written to the remote location
            destination_file (str): The name of the file in the remote location, can be different from the source file
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
            # The destination bucket and filename on the MinIO server
            # Make the bucket if it doesn't exist.
            found = client.bucket_exists(bucket_name)
            if not found:
                client.make_bucket(bucket_name)
                logging.info("Created bucket", bucket_name)
            else:
                logging.info("Bucket", bucket_name, "already exists")
                # Upload the file, renaming it in the process
                client.fput_object(bucket_name, destination_file, source_file)
                logging.info( source_file, "successfully uploaded as object", destination_file, "to bucket", bucket_name)

        except :
            logging.error("There was a problem connecting to your remote bucket. Check connection parameters and try again!")
        
        return 
        