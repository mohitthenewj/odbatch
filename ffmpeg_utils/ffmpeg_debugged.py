import ffmpeg
import re
import os
from os import listdir
from os.path import isfile, join
# from multiprocessing import set_start_method
import multiprocessing as mp

import concurrent.futures   
from ast import literal_eval
import sys
from timer import timer
import tracemalloc
import gc

# stream = ffmpeg.input(f"./blob_vid/13335.mp4")
# stream = ffmpeg.filter(stream,'trim', duration=20)
# stream = ffmpeg.filter(stream,'fps', fps=1, round='up')
# stream = ffmpeg.output(stream, f"./1335.mp4")
# ffmpeg.run(stream)


# print(files[0])
# with open ('./list_vids.txt','r') as f:
#     files  = literal_eval(f.read())

files = [f.split('.')[0] for f in listdir('./blob_vid') if re.search('\d+\.mp4',f)]
files = files[400:500]
print(len(files))
# print(files[-50:-1])

#############################

from collections import Counter
import linecache
import os
import tracemalloc

def display_top(snapshot, key_type='lineno', limit=3):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        print("#%s: %s:%s: %.1f KiB"
              % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))
###################################

def preprocess(video_id):
# mp.set_start_method("spawn", force=True)
# if isfile(f'./blob_vid/{video_id}_.mp4'):
# print(f'file already exists')
# pass
# else:
    
    stream = ffmpeg.input(f"./blob_vid/{video_id}.mp4")
    stream = ffmpeg.filter(stream,'trim', duration=10)
    stream = ffmpeg.filter(stream,'fps', fps=1, round='up')
    stream = ffmpeg.output(stream, f"./blob_vid/{video_id}_.mp4")
    # print(f'4 >>>> {sys.getsizeof(stream)}')
    ffmpeg.run(stream)
    # stream = ffmpeg.input(f"./blob_vid/{video_id}.mp4").video.filter('trim', duration=10).filter('fps', fps=1.0, round='up').output(f'./blob_vid/{video_id}_.mp4')
    # ffmpeg.run(stream)
    print(f'saved at >> ./blob_vid/{video_id}_.mp4')
    gc.collect()


tracemalloc.start()

preprocess('16525')

snapshot = tracemalloc.take_snapshot()
display_top(snapshot)

# @timer(1,1)
# def main():
#     p = mp.Pool(5)
#     p.map(preprocess, files)
# #     with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
# #         executor.map(preprocess, files)
# #         executor.shutdown(wait=True)

