from .material import *
from utils import *
from ray import *

class Metal(Material):
  def __init__(self, albedo, fuzz = 1.0):
    self.albedo = albedo
    self.fuzz = fuzz if (fuzz < 1.0) else 1.0

  def scatter(self, ray, hitrec):
    reflected = reflect(unit_vector(ray.direction), hitrec.normal)
    scattered = Ray(hitrec.p, reflected + self.fuzz * random_in_unit())
    return (np.dot(scattered.direction, hitrec.normal) > 0.0), scattered, self.albedo