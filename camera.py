import numpy as np
from ray import *

class Camera:
  def __init__(self,
               low_left_corner = np.array([-2.0, -1.0, -1.0]),
               horizontal = np.array([4.0, 0.0, 0.0]),
               vertical = np.array([0.0, 2.0, 0.0]),
               origin = np.array([0.0, 0.0, 0.0])
               ):
    self.low_left_corner = low_left_corner
    self.horizontal = horizontal
    self.vertical = vertical
    self.origin = origin

  def getRay(self, u, v):
    return Ray(self.origin, self.low_left_corner + u * self.horizontal + v * self.vertical)
