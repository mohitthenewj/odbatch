import re
import os
from tqdm import tqdm
from os import listdir
from os.path import isfile, join
from ast import literal_eval


# files = [f.split('.')[0] for f in listdir('./vids/') if re.search('\d+\_.mp4',f)]
# files = [f.split('.')[0] for f in listdir('./vids/') if os.path.getsize(f'./vids/{f}')>100]

#  find ./vids -type f -name '*_.mp4' -exec du -ch {} + | grep total$

files = [] 
for f in tqdm(listdir('./vids/')):
    #  pattern for file like 1234_.mp4
    if re.search('\d+\_$',f[:-4]) and os.path.getsize(f'./vids/{f}') == 0:
        files.append(f.split('.')[0])

print(f'len of files is {len(files)}')

###########################################
