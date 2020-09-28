from azure.cosmos import CosmosClient
import os
import json
import pandas as pd

# JSON to pandas util

CONFIG = {
    "ENDPOINT": "https://cosmos-ml.documents.azure.com:443/",
    "PRIMARYKEY": "Xk2aRRmk45Ix6CJH72ZgzcbV0uQn4Ln2gYnAfdPY4gxi65X2odyA9BdIxlCWBkiWquodWSyHY7mFce1L5X9Nzg==",
    "DATABASE": "pipeline",  
    "CONTAINER": "custom_od"
}

url = CONFIG["ENDPOINT"]
key = CONFIG["PRIMARYKEY"]
client = CosmosClient(url, credential=key)

database_name = 'pipeline'
database = client.get_database_client(database_name)
container_name = 'custom_od'
container = database.get_container_client(container_name)

odData = list(container.query_items(
        query='SELECT * FROM c',
        enable_cross_partition_query=True))

#print(len(odData))
# Duplicate removal
fold_list=[]
main_obj =[]
for i in odData:
    if i['video']['folder'] not in fold_list:
        fold_list.append(i['video']['folder'])
        main_obj.append(i)

odData = main_obj
objectList = []
for video in odData:
    allFrames = []
    for frame in video['ml-data']['object-detection']['frames']:
#         allFrames.extend(frame['objects'])
        for obj in frame['objects']:
            obj['frame'] = frame['frame']
            if obj['score'] > 0.8:
#                 print(obj)
                allFrames.append(obj)
    for item in allFrames:
        item['folder'] = video['video']['folder']
        item['id'] = video['id']
    
    objectList.append(allFrames)
    
flat_list = [item for sublist in objectList for item in sublist]

odDf = pd.DataFrame(flat_list)
odDf = odDf.sort_values(by=['folder', 'frame'])


odDf.to_csv("od_data_json_update.csv")


