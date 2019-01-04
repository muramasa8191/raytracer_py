from material.material import Material
from utils import random_in_unit
from ray import *

class Lambertian(Material):
  def __init__(self, albedo):
    self.albedo = albedo

  def scatter(self, ray, hitrec):
    target = hitrec.p + hitrec.normal + random_in_unit()
    return True, Ray(hitrec.p, target - hitrec.p), self.albedo