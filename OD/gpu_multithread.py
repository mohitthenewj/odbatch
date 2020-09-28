from multiprocessing import Pool, current_process, Queue
from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm
from flask_app import object_d2
from os import listdir
from os.path import isfile, join
import re
import os
from timer import timer
import timeit

# Multithread implementation of OD, work in progress

# start = timeit.default_timer()
# NUM_GPUS = 1
# PROC_PER_GPU = 3
# queue = Queue()



def main_func(file):
    if isfile(f'./blob_vid/{file}.mp4'):
        print(f'file already exists')
        pass
    else: 
        # run processing on GPU <gpu_id>
        # print('{}: starting process on GPU {}'.format(ident, gpu_id))
        print(f"Processing {file}.mp4")
        object_d2(file)
        # ... process filename
        print('{}: finished'.format(ident))


files = [f.split('.')[0] for f in listdir('./blob_vid') if re.search('.+_.mp4',f)]
# object_d2(files[0])
# print(files[0])
@timer(1,1)
def samp():
    for file in tqdm(files):
        object_d2(file[:2])

# print(files[0])
# # initialize the queue with the GPU ids
# @timer(1,1)
# def main():
#     with ThreadPoolExecutor(max_workers=20) as executor:

#         outs = executor.map(main_func, files[:50])
#         executor.shutdown(wait=True)

# print(files[0])
# from pathlib import Path
# Path('somefile.txt').stat()
# os.stat_result(st_mode=33188, st_ino=6419862, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1564, st_atime=1584299303, st_mtime=1584299400, st_ctime=1584299400)
# print(Path(f'./blob_vid/{files[0]}').stat().st_size)
