#!/bin/bash

prefix="$1" #ex. hb_r

#get 2d point for all videos in folder
cd VideoPose3D/inference && python3 infer_video_d2.py --cfg COCO-Keypoints/keypoint_rcnn_R_101_FPN_3x.yaml --output-dir ../../"$prefix"_outputs  --image-ext mp4 ../../"$prefix"/
cd VideoPose3D/data/ && python3 prepare_data_2d_custom.py -i ../../"$prefix"_outputs -o "$prefix"_dataset