#to calculate angles between joints

import numpy as np
import math
import json

body_25_num_joints = 25

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
def calculate_angles(angle_jgroup, coordinates):
    angles = []
    for j in angle_jgroup:
        s,c,e = j
        s_hat = coordinates[s] - coordinates[c]
        c_hat = coordinates[c] - coordinates[c]
        e_hat = coordinates[e] - coordinates[c]
        alpha = math.acos((s_hat*e_hat)/(np.linalg.norm(s_hat)*np.linalg.norm(e_hat)))
        angles.append(alpha)
    return angles

def testing(ij):
    with open(ij) as json_file:
        frame = json.load(json_file)

    coord = frame['people'][0]['pose_keypoints_2d']
    coord = {(k/3):np.array([coord[k:k+2]]) for k in range(0, len(coord),3)}

    calculate_angles(bt_joints, coord)


testing('sample_output.json')