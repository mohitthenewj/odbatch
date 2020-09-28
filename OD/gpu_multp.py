from multiprocessing import Pool, current_process, Queue

from flask_app import object_d2
from os import listdir
from os.path import isfile, join

from timer import timer
import timeit

start = timeit.default_timer()

NUM_GPUS = 1
PROC_PER_GPU = 3

queue = Queue()

def main_func(file):
    if isfile(f'./blob_vid/{file}.mp4'):
        print(f'file already exists')
        pass
    else: 
        gpu_id = queue.get()
        try:
            # run processing on GPU <gpu_id>
            ident = current_process().ident
            print('{}: starting process on GPU {}'.format(ident, gpu_id))
            object_d2(file)
            # ... process filename
            print('{}: finished'.format(ident))
        except Exception as e:
            print(e)
        finally:
            queue.put(gpu_id)

# initialize the queue with the GPU ids
for gpu_ids in range(NUM_GPUS):
    for _ in range(PROC_PER_GPU):
        queue.put(gpu_ids)

pool = Pool(processes=PROC_PER_GPU * NUM_GPUS)
files = [f.split('.')[0] for f in listdir('./blob_vid') if isfile(join('./blob_vid', f)) and f.split('_')[-1] == '.mp4' and not f.startswith('.mp4')]
files = files[:100]

for _ in pool.imap_unordered(main_func, files):
    pass
pool.close()
pool.join()

stop = timeit.default_timer()

print('Total time taken was >>>>: ', stop - start)  
# Total time taken was >>>>:  1682.9120022839998



