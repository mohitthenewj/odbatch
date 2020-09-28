#  lib imports
import re
from tqdm import tqdm
from timer import timer
from os.path import isfile, join, isdir
import ffmpeg

# from ast import literal_eval
# from multiprocessing import set_start_method
# from os import listdir
# from os.path import isfile, join
# import concurrent.futures   


# Main utility for trim and duration reduction

def preProcess(video_id = None, basepath = None, video_folder = None, out_folder = None, trim_duration=10,fps=1 ):
    '''
    Parameters
    ----------
    video_id : e.g. 11234, should not include any extensions
    basepath : absolute or relative path, must not end with slash("/"), e.g. /users/mnt
                can be same as current work dir
    video_folder : Meta videos should be stored inside this folder, must followed by basepath, 
                    e.g. /user/mnt/{video_folder}
    out_folder = videos output should be stored inside this folder, must followed by basepath, 
                    e.g. /user/mnt/{out_folder}

    '''
    assert isfile(f'{basepath}/{video_folder}/{video_id}.mp4'),  'File does not exists or wrong path'
    assert isdir(f'{basepath}/{out_folder}'),  'Directory does not exists or wrong path'

    if isfile(f'{basepath}/{video_folder}/{video_id}_.mp4'):
        print(f'file already exists')
        pass
    else: 
        # os.remove(f'{basepath}/{video_folder}/{video_id}.mp4')
        (
            ffmpeg
            .input(f'{basepath}/{video_folder}/{video_id}.mp4')
            .filter('trim', duration= trim_duration)    
            .filter('fps', fps=fps, round='up')
            .output(f'{basepath}/{out_folder}/{video_id}_.mp4')
            .run(overwrite_output= True)
        )
        print("process finished")

# load list of file name from txt files

# with open('/data/mnt_data/kubenetra/integration/ls_blobs_name.txt') as file:
#     vid_list = literal_eval(file.read())

# file name==pitch ID that contains mp4 extensions

# Load list of files ID from path
# files = [f.split('.')[0] for f in listdir('./vids/') if re.search('\d+\.mp4',f)]

# for file in tqdm(files):
#     preProcess(file)

# Utility for multiprocessing, not recommended 
# @timer(1,1)
# def main():
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         executor.map(preProcess, vid_list)
#         executor.shutdown(wait=True)


if __name__=='__main__':
    preProcess(video_id='1335', basepath='/data1/code_base/mnt_data/ODbatch/', video_folder='vids', out_folder='outf')
