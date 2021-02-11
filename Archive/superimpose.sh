#!/bin/bash

querypath="$1"
vidfn="$2"
outputdir="$3"

cd openpose && ./build/examples/openpose/openpose.bin --video=$querypath/$vidfn.mp4 --write_json ./output/$outputdir --display 0  --write_video ../$vidfn.avi
  # convert the result into MP4
ffmpeg -y -loglevel info -i $vidfn.avi $vidfn.mp4