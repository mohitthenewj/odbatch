import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import azure.cosmos.http_constants as http_constants
from azure.cosmos.partition_key import PartitionKey

import os


# Container create and delete util for Cosmos DB

CONFIG = {
    "ENDPOINT": "https://cosmos-ml.documents.azure.com:443/",
    "PRIMARYKEY": "Xk2aRRmk45Ix6CJH72ZgzcbV0uQn4Ln2gYnAfdPY4gxi65X2odyA9BdIxlCWBkiWquodWSyHY7mFce1L5X9Nzg==",
    "DATABASE": "pipeline",  # Prolly looks more like a name to you
    "CONTAINER": "custom_od"  # Prolly looks more like a name to you
#     "CONTAINER": "object_detection"  # Prolly looks more like a name to you
}

url = CONFIG['ENDPOINT']
key = CONFIG['PRIMARYKEY']
client = cosmos_client.CosmosClient(url, {'masterKey': key})

database_id = CONFIG["DATABASE"]
container_id = CONFIG["CONTAINER"]

# partition_key=PartitionKey(path='/language')


database = client.get_database_client(database_id)

containers = database.list_containers()

#database.delete_container(CONFIG['CONTAINER'])
print("done")

database.create_container_if_not_exists(id='custom_od', partition_key=PartitionKey(path="/category"))
