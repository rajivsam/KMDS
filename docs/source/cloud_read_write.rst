Reading from and Writing to the Cloud
########################################

Reading From Cloud End Points
******************************
There are two examples of reading from cloud endpoints that are provided.  The reader modules for cloud storage providers are listed in the `cloud readers folder <https://github.com/rajivsam/KMDS/tree/main/kmds/cloud_readers>`_ in the source directory. You may want to do this for reasons such as the following:

1. Receive a data file from a colleague in a project, for example, someone from the product or business team, giving you a raw dataset for analysis.

2. Recieve a file containing data products such as *embeddings* and *annotated data* produced by another team that you want to consume in your modeling.

S3 is one of the most prevalent storage options for this type of exchange. Minio abstracts away the vendor dependency on S3 storage so you can move your S3 resources between cloud providers. `Minio <https://min.io/>`_ provides such an implementation. See `this minio sandbox video <https://www.youtube.com/watch?v=-r6UsTNGZcg&t=88s>`_ for details of using minio with python. See `the minio reader notebook <https://github.com/rajivsam/KMDS/blob/main/examples_of_use/cloud/minio_cloud_reader.ipynb>`_ for details of using minio with kmds.

Dropbox is another option to read files from. Dropbox supports `OAuth2 <https://oauth.net/2/>`_. An example of using the box python sdk to read files from dropbox is provided in `the box reader <https://github.com/rajivsam/KMDS/blob/main/examples_of_use/cloud/box_connector.ipynb>`_ example.

Examples are provided for two storage providers, other storage providers can be supported similarly. 


Writing to Cloud End Points
****************************

Data science teams can produce data products, such as labeled data, and features from models (for example from an autoencoder or your favorite language model), that they may want to share with other teams who may consume them in their applications, or, perform search on these products in their applications. Since S3 is the most commonly used storage option, a Minio writer is provided as a start. It is possible to extend both the reader and the writer interface to support other storage providers. Please see `the minio writer <https://github.com/rajivsam/KMDS/blob/main/examples_of_use/cloud/minio_cloud_writer.ipynb>`_ for the details of using the writer interface to write to cloud storage.


