#to calculate angles between joints

import numpy as np
import math
import json

bt_joints = [
    [8,1,0],
    [2,1,5],
    [1,2,3],
    [2,3,4],
    [1,5,6],
    [5,6,7],
    [8,9,10],
    [9,10,11],
    [8,12,13],
    [12,13,14],
    [4,8,7],
    [11,8,14],
    [4,8,1],
    [1,8,7]
]
#note that the returned angle will be in radians
#where coordinates is a numpy array
def calculate_angles(joints, coordinates):
    for j in joints:
        s,c,e = j
        s =
        angle = math.acos()

def testing(ij):
    with open(ij) as json_file:
        frame = json.load(json_file)

    coordintes = frame['pose_keypoints_2d']
    calculate_angles(bt_joints, )


calculate_angles()