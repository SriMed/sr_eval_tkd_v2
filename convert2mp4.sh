#!/bin/bash

for f in *
do
	vidfn=$(basename $f .MOV)
	echo "$vidfn"
#	ls
  ffmpeg -i "$f" -q:v 0 ../TestSet2/"$vidfn".mp4
done