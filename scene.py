import numpy as np
import random
import time
from utils import unit_vector
from PIL import Image

class Scene(object):
  def __init__(self, nx, ny, ns, camera):
    self.nx = nx
    self.ny = ny
    self.ns = ns
    self.camera = camera

  def render(self, objects):
    print("start rendering... nx={0}, ny={1}, ns={2}, object size={3}".format(self.nx, self.ny, self.ns, len(objects.objects)))
    img_arr = []
    for j in range(self.ny-1, -1, -1):
      row = []
      for i in range(self.nx):
        col = np.array([0.0, 0.0, 0.0])
        for _s in range(self.ns):
          u = (float(i) + random.uniform(0.0, 1.0)) / self.nx
          v = (float(j) + random.uniform(0.0, 1.0)) / self.ny
          ray = self.camera.getRay(u, v)
          col += color(ray, objects, 0)
        col /= self.ns 
        col = np.sqrt(col)
        row.append([col[0] * 255.0, col[1] * 255.0, col[2] * 255.0])
      img_arr.append(row)
      print ("\r{0:d} / {1:d} done...".format(self.ny - (j), self.ny), end="")
    print("\rcomplete!             ", end="")

    end = time.time()

    img = Image.fromarray(np.uint8(np.array(img_arr)))
    img.show()

    return end

def sky(ray):
  unit_dir = unit_vector(ray.direction)
  t = 0.5 * (unit_dir[1] + 1.0)
  return (1.0 - t) * np.array([1.0, 1.0, 1.0]) + t * np.array([0.5, 0.7, 1.0])

def color(ray, objects, depth):
  is_hit, hitrec = objects.hit(ray, 0.001, 9999999)
  if (is_hit):
    if (depth < 50):
      is_scatter, scattered, attenuation = hitrec.material.scatter(ray, hitrec)
      if (is_scatter):
        return attenuation * color(scattered, objects, depth + 1)
    return np.array([0.0, 0.0, 0.0])
  return sky(ray)
