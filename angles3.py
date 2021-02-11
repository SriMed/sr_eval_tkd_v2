#to calculate angles between joints
#note that math returns angles in radians
import numpy as np
import math
import json
import pickle

h36m_num_joints = 17
h36m_joints = {
    0: [7,8,9],
    1: [14,8,11],
    2: [8,14,15],
    3: [14,15,16],
    4: [8,11,12],
    5: [11,12,13],
    6: [7,1,2],
    7: [1,2,3],
    8: [7,4,5],
    9: [4,5,6],
    10: [16,7,13],
    11: [3,7,6],
    12: [8,7,16],
    13: [8,7,13]
}

#note that the returned angle will be in radians
#where coordinates is a numpy array
def calc_angle(angle_jgroup, coordinates):
    angles = np.array([])
    for i in angle_jgroup:
        s,c,e = angle_jgroup[i]
        s_hat = coordinates[s] - coordinates[c]
        c_hat = coordinates[c] - coordinates[c]
        e_hat = coordinates[e] - coordinates[c]

        dot_product = s_hat@e_hat
        alpha = math.acos((dot_product)/(np.linalg.norm(s_hat)*np.linalg.norm(e_hat)))

        angles = np.append(angles, alpha)
    return angles

#given filename with frame.json, gets angles
def get_frame_angles(frame):
    ang = calc_angle(h36m_joints, frame)
    return ang

def get_angles(data):
    ang = np.empty((len(data),len(h36m_joints)))
    for i, d in enumerate(data):
        f_ang = get_frame_angles(d)
        ang[i] = f_ang
    return ang

data = np.load('xy_Static/hb_ll_9.npy')
# print(data)
ang = get_angles(data)
print(ang)