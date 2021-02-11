#!/bin/bash

prefix="$1" #folder of videos you want to get 3d poses for

# shellcheck disable=SC2045
# shellcheck disable=SC2006
for f in `ls "$prefix"`
do
	vidfn="${f%.*}"
	#get 3d outputs, video + .npy
	cd VideoPose3D/ && python run.py -d custom -k "$prefix"_dataset -arc 3,3,3,3,3 -c checkpoint --evaluate pretrained_h36m_detectron_coco.bin --render --viz-subject f --viz-action custom --viz-camera 0 --viz-video ../"$prefix"/f --viz-output "$vidfn"_si.mp4 --viz-export "$vidfn"_si --viz-size 6
done