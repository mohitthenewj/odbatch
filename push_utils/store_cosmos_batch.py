import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import azure.cosmos.http_constants as http_constants
import argparse
from pathlib import Path
import os
import json
from tqdm import tqdm

from ast import literal_eval
from os import listdir
from os.path import isfile, join
import concurrent.futures
from timer import timer

# azure-core==1.8.0
# azure-cosmos==4.0.0
# azure-storage-blob==12.1.0


COSMOS_ACCOUNT_URI="https://cosmos-ml.documents.azure.com:443"
COSMOS_ACCOUNT_KEY="Xk2aRRmk45Ix6CJH72ZgzcbV0uQn4Ln2gYnAfdPY4gxi65X2odyA9BdIxlCWBkiWquodWSyHY7mFce1L5X9Nzg=="

client = cosmos_client.CosmosClient(url = COSMOS_ACCOUNT_URI, credential = COSMOS_ACCOUNT_KEY)

database_name = 'pipeline'
database = client.get_database_client(database_name)
container_name = 'custom_od'
container = database.get_container_client(container_name)

# get list of files for upload 

        
#  Push util for COSMOS JSON
def push_files(files, basepath = None):
    for file in tqdm(files):
        with open(f'{basepath}/{file}.json', 'rb') as f:
            data = json.load(f)
            container.upsert_item(data)
            print('Upload completed for {">"*10} {file}')

basepath = f'/data1/code_base/mnt_data/kubenetra/integration/json'
files = []
for f in listdir(f'{basepath}/'):
    if '.json' in f and os.path.getsize(f'{basepath}/{f}') != 0:
        files.append(f.split('.')[0])
