import ffmpeg
import re
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from tqdm import tqdm


def pull_main(video_id = '', output_file='10056.mp4', \
connection_string = "DefaultEndpointsProtocol=https;AccountName=videobank;AccountKey=+7+BZaxs5zBHwyDAMJHnMEJS1mhzIN4AC6PS7wIbVgE1hd35eHEB9IAbc+E2PfV4GNP7dkFrWiLAVMZ8HgnFEw==;EndpointSuffix=core.windows.net", \
container_client = 'athenaliveprod', lang = 'hindi'):
    connect_str = connection_string
    video_id = video_id
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    container = blob_service_client.get_container_client(container_client)

    blobs = container.list_blobs(name_starts_with=f'athenaliveprod/')
    pat_format = re.compile('.*\.mp4')
    pat_lang = re.compile(f'.*{lang}', re.IGNORECASE)
    all_vids = []
    for b in tqdm(blobs):
        
        name_blob = b.name
        if re.search(pat_format,name_blob) and re.search(pattern=pat_lang, string=name_blob):
            vid_id = name_blob.split('/')[1]
            all_vids.append(vid_id)
    print(f'Total video num is {len(all_vids)}')
    print(f'Total video num is {list(set(all_vids[:20]))}')
    with open('list_vids.txt', 'w') as file:
        file.write(str(list(set(all_vids))))
pull_main()