import argparse
import glob
import multiprocessing as mp
import os
import cv2
import time
from tqdm import tqdm
import json 
import ffmpeg
from functools import reduce
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import re
import os
from os import listdir
from os.path import isfile, join
from ast import literal_eval
import sys



import base64
import numpy as np
import io
from PIL import Image
# from flask import request
# from flask import jsonify
# from flask import Flask

from detectron2.config import get_cfg
from detectron2.data.detection_utils import read_image
from detectron2.utils.logger import setup_logger

from predictor import VisualizationDemo

# constants
WINDOW_NAME = "COCO detections"


def setup_cfg(args):
    cfg = get_cfg()
    cfg.merge_from_file(args.config_file)
    
    # cfg.MODEL.WEIGHTS = '/app/model_final_nate.pkl'
    cfg.MODEL.WEIGHTS = '/data/work/colab_d2_copy/colab_d2/model_final_nate.pkl'
    # Set score_threshold for builtin models
    cfg.MODEL.RETINANET.SCORE_THRESH_TEST = 0.5 #args.confidence_threshold
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5 #args.confidence_threshold
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = args.confidence_threshold
    cfg.freeze()
    return cfg


def get_parser():
    parser = argparse.ArgumentParser(description="Detectron2 demo for builtin models")
    parser.add_argument(
        "--config-file",
        # default = '/app/docker_files/detectron2/configs/Misc/panoptic_fpn_R_101_dconv_cascade_gn_3x.yaml',
        default = '/data/work/colab_d2_copy/colab_d2/docker_files/detectron2/configs/Misc/panoptic_fpn_R_101_dconv_cascade_gn_3x.yaml',
        metavar="FILE",
        help="path to config file",
    )
    parser.add_argument("--webcam", action="store_true", help="Take inputs from webcam.")
    parser.add_argument("--video-input", default = '/app/detectron2/demo/new_clip.mp4', help="Path to video file.")
    parser.add_argument("--fps", default = 1, help="Pass along the FPS.")
    parser.add_argument(
        "--input",
        nargs="+",
        # default = './archive/video-clip_1.mp4'
        help="A list of space separated input images; "
        "or a single glob pattern such as 'directory/*.jpg'",
    )
    parser.add_argument(
        "--output",
        default = './out_new.mp4',
        help="A file or directory to save output visualizations. "
        "If not given, will show output in an OpenCV window.",
    )

    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.5,
        help="Minimum score for instance predictions to be shown",
    )
    parser.add_argument(
        "--opts",
        help="Modify config options using the command-line 'KEY VALUE' pairs",
        default=[],
        nargs=argparse.REMAINDER,
    )
    parser.add_argument(
        "--video_id",
        default='',
        nargs=argparse.REMAINDER,
    )
    return parser

def object_d2(files):
    # mp.set_start_method("spawn", force=True)
    args, unknown = get_parser().parse_known_args()
    setup_logger(name="fvcore")
    logger = setup_logger()
    logger.info("Arguments: " + str(args))

    cfg = setup_cfg(args)
    print("A ...................")
    demo = VisualizationDemo(cfg)
    print("B ...................")
    basepath = '/data1/code_base/mnt_data/kubenetra/integration/vids'
    for video_id in tqdm(files):
        # integration/vids/14686_.mp4
        try:
            print(f'this will be loaded >>>>>>> /mnt/az/kubenetra/blob_vid/{video_id}.mp4')

            video = cv2.VideoCapture(f'{basepath}/{video_id}.mp4')
            print("E>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            # video = cv2.VideoCapture('/app/new_clip_resized_resized.mp4')

            width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            # print(f'width is {width}')
            height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frames_per_second = video.get(cv2.CAP_PROP_FPS)
            img_pixels = height*width
            if frames_per_second ==0:
                pass
            else:
                num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
                print('<<<<<<<<<<<<<<<<<<<<< ',video.get(cv2.CAP_PROP_FRAME_COUNT))
                #######################

                duration = num_frames/frames_per_second
                
                print('num_frames is ',num_frames)
                # print(f'duration is {duration} and fps is {frames_per_second}')

                counter = 0 
                frames=[]
                all_preds = list(demo.run_on_video(video))
                i=1
                total_frames = num_frames
                # while num_frames!=0:
                for num_frame, semantic_predictions in enumerate(all_preds):
                    # semantic_predictions = next(all_preds)
                    # semantic_predictions = item
                    objs = []
                    for s in semantic_predictions:
                        obj = {}
                        obj["label"] = s["text"]
                        obj['area_percentage'] = float("{0:.2f}".format(s['area']/img_pixels))
                        obj["score"] = float("{0:.2f}".format(s["score"] if "score" in s else 1))
                        objs.append(obj)

                    obj_set = {}
                    for s in semantic_predictions:
                        k = s["text"]
                        score = s["score"] if "score" in s else 1
                        if not k in obj_set:
                            obj_set[k] = {
                                "scores": [score],
                                "areas":  [s["area"]],
                                "label": k
                            }
                        else:
                            obj_set[k]["scores"].append(score)
                            obj_set[k]["areas"].append(s["area"])

                    u_objs = []
                    for k in obj_set:
                        u = obj_set[k]
                        n = len(u["scores"])
                        score_ave = reduce((lambda x, y: x + y), u["scores"])/n
                        area_sum = reduce((lambda x, y: x + y), u["areas"])

                        obj = {}
                        obj["label"] = u["label"]
                        obj['area_percentage'] = float("{0:.2f}".format(area_sum/1000000))
                        obj["score"] = float("{0:.2f}".format(score_ave))
                        obj["count"] = n
                        u_objs.append(obj)
                    frame = {
                        "frame":i,
                        "instances": objs,
                        "objects": u_objs,
                    }
                
                    # print('num_frame is ',total_frames - num_frames + 1)
                    print('num_frame is ',num_frame + 1)
                    # counter+=1
                    # num_frames-=1
                    # i+=1
                    frames.append(frame)
                cv2.destroyAllWindows()
                data = {
                    "video": {
                        "meta": {},
                        "base_uri": "https://videobank.blob.core.windows.net/videobank",
                        "folder": args.video_input,
                        "output-frame-path": "pipeline/detectron2"
                    },
                    "ml-data": {
                        "object-detection": {
                            "meta": {'duration':duration, 'fps':frames_per_second,'len_frames':len(frames)},
                            "video": {},
                            "frames": frames
                        }
                    }
                }
                # print(f'data is {data}')
                # try:
                #     os.remove(f'./blob_vid/{video_id}.txt')
                # except OSError:
                #     pass

                # return data
                print(f'writing OD outs inside >>> {basepath}/{video_id}.json')
                with open(f'{basepath}/{video_id}.json', 'w') as f:
                    json.dump(data,f)
        except Exception as e:
            print(e)
            with open('./err_vids.txt','a') as f:
                f.write(str(e))
            pass


files_ffmpeg=[]
for f in listdir('./vids/'):
    if re.search('\d+\_$',f[:-4]) and os.path.getsize(f'./vids/{f}') != 0:
        files_ffmpeg.append(f.split('.')[0])

object_d2(files_ffmpeg)

