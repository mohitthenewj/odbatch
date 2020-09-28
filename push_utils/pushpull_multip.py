  
import argparse
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContentSettings
from os import listdir
from os.path import isfile, join
from timer import timer
import concurrent.futures   
import re
import ffmpeg
import os 
from flask_app import object_d2
from ast import literal_eval



#  Push and pull util for BLOB storage

upload_path = 'pre_process'
content_type = 'video/mp4'
container_pull = 'athenaliveprod'
container_push = 'videobank'

connection_string = 'DefaultEndpointsProtocol=https;AccountName=videobank;AccountKey=+7+BZaxs5zBHwyDAMJHnMEJS1mhzIN4AC6PS7wIbVgE1hd35eHEB9IAbc+E2PfV4GNP7dkFrWiLAVMZ8HgnFEw==;EndpointSuffix=core.windows.net'
lang='hindi'
blob_service_client_pull = BlobServiceClient.from_connection_string(connection_string)
container_client_pull = blob_service_client_pull.get_container_client(container_pull)


blob_service_client_push = BlobServiceClient.from_connection_string(connection_string)
container_client_push = blob_service_client_push.get_container_client(container_push)
contentType = ContentSettings(content_type=content_type)
pat_format = re.compile('.*\.mp4')
pat_lang = re.compile(f'.*{lang}', re.IGNORECASE)

# files = [fl.split('.')[0] for fl in listdir('/mnt/az_p/az_p/kubenetra/blob_vid/') if not fl.startswith('.') ]
# files = ['10078', '10011', '10012', '10076', '10056', '10171', '10184', '10170']

with open('./list_vids.txt') as file:
    files = literal_eval(file.read())
print(files)

defaluter =[]

def push_f(video_id):

    f= f'{video_id}'
    dest = f"{video_id}_tmp/{upload_path}/{f}_.mp4"
    blob_client = container_client_push.get_blob_client(dest)

    with open(f"/mnt/az_p/az_p/kubenetra/blob_vid/{f}_.mp4", "rb") as data:
        print(f"{f} -> {video_id}_tmp/{upload_path}/{f}_.mp4")
        blob_client.upload_blob(data, overwrite=True, content_settings=contentType)


@timer(1,1)
def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(push_f, files[:10])

# print(files[0])
# push_f(files[0])
# for f in files:
#     dest = f"{args.video_id}/{args.upload_path}/{f}"
#     blob_client = container_client.get_blob_client(dest)
#     try:
#         with open(f"{args.input_path}/{f}", "rb") as data:
#             print(f"{f} -> {args.video_id}/{args.upload_path}/{f}")
#             blob_client.upload_blob(data, overwrite=True, content_settings=contentType)
#     except:
#         print("Upload failure")