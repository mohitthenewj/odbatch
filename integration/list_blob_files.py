import re
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from tqdm import tqdm
import concurrent.futures   
from ast import literal_eval
from multiprocessing import set_start_method
from os.path import isfile, join



def pull_main(container_client = 'athenaliveprod', lang = 'hindi', name_starts_with = 'athenaliveprod/', ext = 'mp4'):
    # set_start_method("spawn", force=True)

    # Connection set up 
    connect_str = "DefaultEndpointsProtocol=https;AccountName=videobank;AccountKey=+7+BZaxs5zBHwyDAMJHnMEJS1mhzIN4AC6PS7wIbVgE1hd35eHEB9IAbc+E2PfV4GNP7dkFrWiLAVMZ8HgnFEw==;EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container = blob_service_client.get_container_client(container_client)

    # List of matching files
    blobs = container.list_blobs(name_starts_with=f'{name_starts_with}')
    pat_format = re.compile(f'.*\.{ext}')
    pat_lang = re.compile(f'.*{lang}', re.IGNORECASE)

    list_hindi_vid =[]

    for b in tqdm(blobs):
        name_blob = b.name
        if re.search(pat_format,name_blob) and re.search(pattern=pat_lang, string=name_blob):
            name_blob_sp = name_blob.split('/')
            folder_name = name_blob_sp[1]
            list_hindi_vid.append(folder_name)
            
    return list_hindi_vid
all_files = pull_main()

print(f'Total pitch fetched are {len(all_files)}')
print(f'Total Unique pitch fetched are {len(set(all_files))}')


with open('ls_blobs.txt','w') as f:
    f.write(str(list(set(all_files))))
