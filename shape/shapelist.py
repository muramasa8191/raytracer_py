from .hitable import *
from hitrec import *

class ShapeList(Hitable):
  def __init__(self, list):
    self.objects = list

  def hit(self, ray, t_min, t_max):
    is_hit = False
    closest = t_max
    hitrec = None
    for obj in self.objects:
      hitted, rec = obj.hit(ray, t_min, closest)
      if (hitted):
        is_hit = True
        hitrec = rec
        closest = rec.t
    return is_hit, hitrec