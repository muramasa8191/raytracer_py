import numpy as np
import random
from ray import *
import math
from utils import unit_vector

class Camera:
  def __init__(self, lookfrom, lookat, vup, vfov, aspect, aperture, focus_dist):
    self.lens_radius = aperture / 2.0
    theta = vfov * math.pi / 180
    half_height = math.tan(theta * 0.5)
    half_width = aspect * half_height

    self.origin = lookfrom
    w = unit_vector(lookfrom - lookat)
    u = unit_vector(np.cross(vup, w))
    v = np.cross(w, u)
    self.low_left_corner = lookfrom - half_width * u * focus_dist - half_height * v * focus_dist - w * focus_dist
    self.horizontal = 2 * half_width * u * focus_dist
    self.vertical = 2 * half_height * v * focus_dist
    self.u = u
    self.v = v
    self.w = w

  def getRay(self, s, t):
    rd = self.lens_radius * random_in_unit_disk()
    offset = self.u * rd[0] + self.v * rd[1]
    return Ray(self.origin + offset, self.low_left_corner + s * self.horizontal + t * self.vertical - self.origin - offset)


def random_in_unit_disk():
  p = 2.0 * np.array([random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), 0.0]) - np.array([1.0, 1.0, 1.0])
  if (np.dot(p, p) >= 1.0):
    return p
  return random_in_unit_disk()