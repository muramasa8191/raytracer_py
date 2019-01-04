import numpy as np
import math
import random
import time
from PIL import Image
from ray import *
from shape.sphere import Sphere
from shape.shapelist import ShapeList
from hitrec import HitRec
from utils import unit_vector
from camera import Camera
from material.lambertian import Lambertian
from material.metal import Metal
from material.dielectric import Dielectric
from scene import Scene

def gradation():
  nx = 200
  ny = 100
  img_arr = []
  for j in range(ny-1, -1, -1):
    row = []
    for i in range(nx):
      r = float(i) / nx
      g = float(j) / ny
      b = 0.2
      row.append([r * 255.0, g * 255.0, b * 255.0])
    img_arr.append(row)

  img = Image.fromarray(np.uint8(np.array(img_arr)))

  img.show()

def sky(ray):
  unit_dir = unit_vector(ray.direction)
  t = 0.5 * (unit_dir[1] + 1.0)
  return (1.0 - t) * np.array([1.0, 1.0, 1.0]) + t * np.array([0.5, 0.7, 1.0])

def draw_sky():
  nx = 200
  ny = 100
  low_left_corner = np.array([-2.0, -1.0, -1.0])
  horizontal = np.array([4.0, 0.0, 0.0])
  vertical = np.array([0.0, 2.0, 0.0])
  origin = np.zeros(3, dtype=float)

  img_arr = []
  for j in range(ny-1, -1, -1):
    row = []
    for i in range(nx):
      u = float(i) / nx
      v = float(j) / ny
      ray = Ray(origin, low_left_corner + u * horizontal + v * vertical)
      col = sky(ray)
      row.append([col[0] * 255.0, col[1] * 255.0, col[2] * 255.0])
    img_arr.append(row)

  img = Image.fromarray(np.uint8(np.array(img_arr)))
  img.show()

def drand48():
  return random.uniform(0.0, 1.0)

def createSpheres():
  objects = [Sphere(np.array([0.0, -1000.0, 0.0]), 1000.0, Lambertian(np.array([0.5, 0.5, 0.5])))]
  for a in range(-11, 11):
    for b in range(-11, 11):
      choose_mat = drand48()
      center = np.array([a+0.9*drand48(), 0.2, b+0.9*drand48()])
      base = center - np.array([4.0, 0.2, 0.0])
      if (math.sqrt(np.sum(base * base)) > 0.9):
        if (choose_mat < 0.8):
          objects.append(Sphere(center, 0.2, Lambertian(np.array([drand48() * drand48(), drand48() * drand48(), drand48() * drand48()]))))
        elif (choose_mat < 0.95):
          objects.append(Sphere(center, 0.2, Metal(np.array([0.5 * (1.0 + drand48()), 0.5 * (1.0 + drand48()), 0.5 * drand48()]))))
        else:
          objects.append(Sphere(center, 0.2, Dielectric(1.5)))
  objects.append(Sphere(np.array([0.0, 1.0, 0.0]), 1.0, Dielectric(1.5)))
  objects.append(Sphere(np.array([-4.0, 1.0, 0.0]), 1.0, Lambertian(np.array([0.4, 0.2, 0.1]))))
  objects.append(Sphere(np.array([4.0, 1.0, 0.0]), 1.0, Metal(np.array([0.7, 0.6, 0.5]), 0.0)))

  return ShapeList(objects)

if __name__ == '__main__':
  start = time.time()
  nx = 200
  ny = 100
  ns = 100
  lookfrom = np.array([11.0, 3.0, 3.0])
  lookat = np.array([0.0, 0.0, 0.0])
  vup = np.array([0.0, 1.0, 0.0])
  dist_to_focus = math.sqrt(np.sum((lookfrom - lookat) * (lookfrom - lookat)))
  aperture = 0.3
  camera = Camera(lookfrom, lookat, vup, 20.0, nx/ny, aperture ,dist_to_focus)

  scene = Scene(nx, ny, ns, camera)

  end = scene.render(createSpheres())
  print("\n\n{0} msec".format(end - start))
