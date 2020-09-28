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


# For editing JSON in batches

basepath = f'/data1/code_base/mnt_data/kubenetra/integration/json'
files = []
for f in listdir(f'{basepath}/'):
    if '.json' in f and os.path.getsize(f'{basepath}/{f}') != 0:
        files.append(f.split('.')[0])
        
try:
    for file in tqdm(files):
        with open(f'/data1/code_base/mnt_data/kubenetra/integration/json/{file}.json', 'r') as f:
            data = json.load(f)
        for num, frame in enumerate(data['ml-data']['object-detection']['frames']):
            frame['frame'] = num+1
        with open(f'/data1/code_base/mnt_data/kubenetra/integration/json/{file}.json', 'w') as f:
            json.dump(data,f)

            print(f'process completed for {file}')
except Exception as e:
    print(e)
    print(f'file name is {file}')
