import numpy as np
from scipy.spatial.distance import euclidean
from angles3 import get_angles
from fastdtw import fastdtw

# x = np.array([[1,1], [2,2], [3,3], [4,4], [5,5]])
# y = np.array([[2,2], [3,3], [4,4]])

def compare_sample(ips, oup):
  d = []
  y = get_angles(np.load(oup))
  for i in ips:
    X = get_angles(np.load(i))
    distance, path = fastdtw(X, y, dist=euclidean)
    d.append(distance)
  return d

ips = ['xy_Static/IMG_5002_si.npy', 'xy_Static/fk_rd_0_si.npy']
oup = 'xy_Static/fk_rd_1_si.npy'

print(compare_sample(ips, oup))