  
import argparse
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContentSettings
from os import listdir
from os.path import isfile, join
import re
from tqdm import tqdm
# # Defining and parsing the command-line arguments
# parser = argparse.ArgumentParser(description='My program description')
# parser.add_argument('--video-id', type=str)
# parser.add_argument('--input-path', type=str)
# parser.add_argument('--upload-path', type=str)
# parser.add_argument('--connection-string', type=str)
# parser.add_argument('--content-type', type=str)
# parser.add_argument('--container', type=str)
# args = parser.parse_args()


upload_path = 'pre_process'
content_type = 'video/mp4'
container = 'videobank'
connection_string = 'DefaultEndpointsProtocol=https;AccountName=videobank;AccountKey=+7+BZaxs5zBHwyDAMJHnMEJS1mhzIN4AC6PS7wIbVgE1hd35eHEB9IAbc+E2PfV4GNP7dkFrWiLAVMZ8HgnFEw==;EndpointSuffix=core.windows.net'
# files = [f for f in listdir(args.input_path) if isfile(join(args.input_path, f))]

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container)
contentType = ContentSettings(content_type=content_type)
basepath=f'/data1/code_base/mnt_data/kubenetra/integration/vids'

files_ffmpeg=[]
for f in listdir(f'{basepath}/'):
    if re.search('\d+\_$',f[:-4]) and os.path.getsize(f'{basepath}/{f}') != 0:
        files_ffmpeg.append(f.split('.')[0])
for f in tqdm(files_ffmpeg):
    dest = f"{f[:-1]}/{upload_path}/{f}.mp4"
    blob_client = container_client.get_blob_client(dest)
    try:
        with open(f"{basepath}/{f}.mp4", "rb") as data:
            print(f"{f}.mp4 -> {f[:-1]}/{upload_path}/{f}.mp4")
            blob_client.upload_blob(data, overwrite=True, content_settings=contentType)
    except Excetion as e:
        print(e)
        print("Upload failed")


# for f in files:
#     dest = f"{args.video_id}/{args.upload_path}/{f}"
#     blob_client = container_client.get_blob_client(dest)
#     try:
# #>
#         with open(f"{args.input_path}/{f}", "rb") as data:
#             print(f"{f} -> {args.video_id}/{args.upload_path}/{f}")
#             blob_client.upload_blob(data, overwrite=True, content_settings=contentType)
#     except:
#         print("Upload failure")