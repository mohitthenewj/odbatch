# OD for batch video processing(alternatively flask application can be used for the similar results.)

* This repo contains all required utils for running object detection during batch process.
* Components
  1. pull blobs(pull_utils.py)
  2. ffmpeg_utils(ffmpeg_flask.py)
  3. Od video processing(odmainutil_batch.py)
  4. push utils(store_cosmos_batch.py)

* Set up of detectron 2 will be exactly similar to detectron2 installation for flask application(https://github.com/mohitthenewj/flaskappdetectron2/blob/master/Dockerfile)
* Download model weights for panoptic segmentation for OD(https://github.com/facebookresearch/detectron2/blob/master/MODEL_ZOO.md)
* Direct download link for model weights(https://dl.fbaipublicfiles.com/detectron2/COCO-PanopticSegmentation/panoptic_fpn_R_101_3x/139514519/model_final_cafdb1.pkl)
