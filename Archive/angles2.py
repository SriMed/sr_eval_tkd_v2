#to calculate angles between joints
#note that math returns angles in radians
import numpy as np
import math
import json
import pickle

coco_num_joints = 18
coco_joints = {
    0: [0,1,8],
    1: [0,1,11],
    2: [2,1,5],
    3: [1,2,3],
    4: [2,3,4],
    5: [1,5,6],
    6: [5,6,7],
    7: [1,8,9],
    8: [8,9,10],
    9: [1,11,12],
    10: [11,12,13],
    11: [4,1,7],
    12: [10,1,13],
    13: [1,8,4],
    14: [1,11,7]
}

#note that the returned angle will be in radians
#where coordinates is a numpy array
def calc_angle(angle_jgroup, coordinates):
    angles = {}
    for i in angle_jgroup:
        s,c,e = angle_jgroup[i]
        s_hat = coordinates[s] - coordinates[c]
        c_hat = coordinates[c] - coordinates[c]
        e_hat = coordinates[e] - coordinates[c]

        dot_product = sum(s_hat[0][i]*e_hat[0][i] for i in range(len(s_hat[0])))
        alpha = math.acos((dot_product)/(np.linalg.norm(s_hat)*np.linalg.norm(e_hat)))

        str = f'{alpha}'
        if any(c.isdigit() for c in str) == False:
            # print('nan here?')
            # angles[i] = np.nan
            angles[i] = 0
        else:
            angles[i] = alpha
    return angles

#given filename with frame.json, gets angles
def get_frame_angles(frame):
    ang = calc_angle(coco_joints, frame)
    return ang

def get_angles(data):
    ang = np.array([])
    for d in data:
        f_ang = get_frame_angles(d)
        np.append(ang, f_ang)
    return ang

data = np.load('../xy_Static/hb_ll_9.npy')
print(data)
ang = get_angles(data)
print(ang)