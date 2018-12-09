from .material import *
from utils import *
from ray import *

class Lambertian(Material):
  def __init__(self, albedo):
    self.albedo = albedo

  def scatter(self, ray, hitrec):
    target = hitrec.p + hitrec.normal + random_in_unit()
    return True, Ray(hitrec.p, target - hitrec.p), self.albedo