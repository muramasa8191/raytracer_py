from material.material import Material
from utils import reflect, refract
from ray import Ray
import math
import random
import numpy as np

class Dielectric(Material):
  def __init__(self, ri):
    self.ref_idx = ri

  def scatter(self, ray, hitrec):
    reflected = reflect(ray.direction, hitrec.normal)
    if (np.dot(ray.direction, hitrec.normal) > 0.0):
      outward_normal = -hitrec.normal
      ni_over_nt = self.ref_idx
      cosine = self.ref_idx * np.dot(ray.direction, hitrec.normal) / (math.sqrt(np.sum(ray.direction * ray.direction)))
    else:
      outward_normal = hitrec.normal
      ni_over_nt = 1.0 / self.ref_idx
      cosine = -np.dot(ray.direction, hitrec.normal) / (math.sqrt(np.sum(ray.direction * ray.direction)))
    
    is_refract, refracted = refract(ray.direction, outward_normal, ni_over_nt)
    if (is_refract):
      reflect_prob = schlick(cosine, self.ref_idx)
    else:
      reflect_prob = 1.0
    if (random.uniform(0.0, 1.0) < reflect_prob):
      scattered = Ray(hitrec.p, reflected)
    else:
      scattered = Ray(hitrec.p, refracted)
    
    return True, scattered, np.array([1.0, 1.0, 1.0])

def schlick(cosine, ref_idx):
  r0 = (1.0 - ref_idx) / (1.0 + ref_idx)
  r0 = r0 * r0
  return r0 + (1.0 - r0) * pow(1 - cosine, 5)