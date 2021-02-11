#!/bin/bash

cd openpose

mkdir ./avi_intermediary/
mkdir ./mp4_finals/

for f in `ls ../hb_fl`
do
	vidfn="${f%.*}"
	mkdir ./output/$vidfn && ./build/examples/openpose/openpose.bin --video=../hb_fl/$f --write_json ./output/$vidfn --display 0  --write_video ../avi_intermediary/$vidfn.avi
	# convert the result into MP4
	ffmpeg -y -loglevel info -i ../avi_intermediary/$vidfn.avi ../mp4_finals/$vidfn.mp4
done