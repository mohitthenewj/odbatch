
# import ffmpeg
import re
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from tqdm import tqdm
from timer import timer
import concurrent.futures   
from ast import literal_eval
from multiprocessing import set_start_method
from os.path import isfile, join


with open('./list_vids.txt') as file:
    vid_list = literal_eval(file.read())
# vid_list = vid_list

def pull_main(video_id = '', output_file='10056.mp4', \
connection_string = "DefaultEndpointsProtocol=https;AccountName=videobank;AccountKey=+7+BZaxs5zBHwyDAMJHnMEJS1mhzIN4AC6PS7wIbVgE1hd35eHEB9IAbc+E2PfV4GNP7dkFrWiLAVMZ8HgnFEw==;EndpointSuffix=core.windows.net", \
container_client = 'athenaliveprod', lang = 'hindi'):
    if isfile(f'./blob_vid/{video_id}.mp4'):
        print(f'file already exists')
        pass
    else: 
        set_start_method("spawn", force=True)
        connect_str = connection_string
        video_id = video_id
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        container = blob_service_client.get_container_client(container_client)

        blobs = container.list_blobs(name_starts_with=f'athenaliveprod/{video_id}')
        pat_format = re.compile('.*\.mp4')
        pat_lang = re.compile(f'.*{lang}', re.IGNORECASE)

        for b in blobs:
            name_blob = b.name
            if re.search(pat_format,name_blob) and re.search(pattern=pat_lang, string=name_blob):
                print('<<<<<    BLOB MATCH FOUND  s >>>>')
                print(f"Downloading {video_id}.mp4")
                downloader = container.download_blob(b)
                file_name = name_blob.split('/')[-1]
                with open(f"./blob_vid/{video_id}.mp4", 'wb') as f:
                    downloader.readinto(f)
                break

@timer(1,1)
def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(pull_main, vid_list)
        executor.shutdown(wait=True)
