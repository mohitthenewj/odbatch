import ffmpeg
import re
import os
from os import listdir
from os.path import isfile, join
from multiprocessing import set_start_method
import concurrent.futures   
from timer import timer
from ast import literal_eval
import asyncio


# Asynchronous implementation of FFMPEG utility

# files = [f.split('.')[0] for f in listdir('./blob_vid') if re.search('\d+\.mp4',f)]
# print(files[0])
with open ('./list_vids.txt','r') as f:
    files  = literal_eval(f.read())

print(files[0])
async def preprocess(video_id):
        set_start_method("spawn", force=True)
        if isfile(f'./blob_vid/{video_id}_.mp4'):
            print(f'file already exists')
            pass
        else:
            stream = ffmpeg.input(f"./blob_vid/{video_id}.mp4")
            stream = ffmpeg.filter(stream,'trim', duration=10)
            stream = ffmpeg.filter(stream,'fps', fps=1, round='up')
            stream = ffmpeg.output(stream, f"./blob_vid/{video_id}_.mp4")
            await ffmpeg.run(stream)
        # stream = ffmpeg.input(f"./blob_vid/{video_id}.mp4").video.filter('trim', duration=10).filter('fps', fps=1.0, round='up').output(f'./blob_vid/{video_id}_.mp4')
        # ffmpeg.run(stream)
        print(f'saved at >> ./blob_vid/{video_id}_.mp4')

# preprocess(files[0])
@timer(1,1)
def main():
     with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(preprocess, files[:50])
        executor.shutdown(wait=True)

