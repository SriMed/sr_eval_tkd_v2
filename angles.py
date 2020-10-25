#to calculate angles between joints


#note that math returns angles in radians
import numpy as np
import math
import json

body_25_num_joints = 25

bt_joints = {
    0: [8,1,0],
    1: [2,1,5],
    2: [1,2,3],
    3: [2,3,4],
    4: [1,5,6],
    5: [5,6,7],
    6: [8,9,10],
    7: [9,10,11],
    8: [8,12,13],
    9: [12,13,14],
    10: [4,8,7],
    11: [11,8,14],
    12: [4,8,1],
    13: [1,8,7]
}

#note that the returned angle will be in radians
#where coordinates is a numpy array
def calculate_angles(angle_jgroup, coordinates):
    angles = {}
    for i in angle_jgroup:
        s,c,e = angle_jgroup[i]
        s_hat = coordinates[s] - coordinates[c]
        c_hat = coordinates[c] - coordinates[c]
        e_hat = coordinates[e] - coordinates[c]

        dot_product = sum(s_hat[0][i]*e_hat[0][i] for i in range(len(s_hat[0])))
        alpha = math.acos((dot_product)/(np.linalg.norm(s_hat)*np.linalg.norm(e_hat)))
        angles[i] = alpha
    return angles

def testing(ij):
    with open(ij) as json_file:
        frame = json.load(json_file)

    coord = frame['people'][0]['pose_keypoints_2d']
    coord = {(k/3):np.array([coord[k:k+2]]) for k in range(0, len(coord),3)}

    ang = calculate_angles(bt_joints, coord)
    print(ang)


testing('sample_output.json')