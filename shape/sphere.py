import numpy as np
from .hitable import *
from hitrec import *

class Sphere(Hitable):
  def __init__(self, pos, r, material=None):
    self.center = np.array(pos)
    self.radius = r
    self.material = material

  def hit(self, ray, t_min, t_max):
    oc = ray.origin - self.center
    a = np.dot(ray.direction, ray.direction)
    b = np.dot(oc, ray.direction)
    c = np.dot(oc, oc) - self.radius * self.radius
    discriminant = b * b - a * c

    if (discriminant > 0.0):
      root = (-b -np.sqrt(discriminant)) / a
      if t_min < root and root < t_max:
        p = ray.at(root)
        return True, HitRec(root, p, (p - self.center) / self.radius, self.material)
      root = (-b + np.sqrt(discriminant)) / a
      if t_min < root and root < t_max:
        p = ray.at(root)
        return True, HitRec(root, p, (p - self.center) / self.radius, self.material)
    return False, None

  def hit1(self, ray):
    oc = ray.origin - self.center
    a = np.dot(ray.direction, ray.direction)
    b = 2.0 * np.dot(oc, ray.direction)
    c = np.dot(oc, oc) - self.radius * self.radius
    discriminant = b * b - 4 * a * c

    return discriminant > 0.0

  def hit2(self, ray):
    oc = ray.origin - self.center
    a = np.dot(ray.direction, ray.direction)
    b = 2.0 * np.dot(oc, ray.direction)
    c = np.dot(oc, oc) - self.radius * self.radius
    discriminant = b * b - 4 * a * c

    if (discriminant < 0.0):
      return -1.0

    return (-b - np.sqrt(discriminant)) / (2.0 * a)