import numpy as np
from PIL import Image
from ray import *
from shape.sphere import *
from shape.shapelist import *
from hitrec import *
import random
import time
from utils import *
from camera import *
from material.lambertian import *
from material.metal import *

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

def color_s(ray, sphere):
  if (sphere.hit1(ray)):
    return [1.0, 0.0, 0.0]
  return sky(ray)

def color_s2(ray, sphere):
  t = sphere.hit2(ray)
  if (t > 0.0):
    n = unit_vector(ray.at(t) - np.array([0.0, 0.0, -1.0]))
    return 0.5 * (n + 1.0)
  return sky(ray)

def color2(ray, objects):
  is_hit, hitrec = objects.hit(ray, 0.001, 99999999)
  if (is_hit):
    return 0.5 * (hitrec.normal + np.array([1.0, 1.0, 1.0]))
  return sky(ray)    

def color3(ray, objects):
  is_hit, hitrec = objects.hit(ray, 0.001, 9999999)
  if (is_hit):
    target = hitrec.p + hitrec.normal + random_in_unit()
    return 0.5 * color3(Ray(hitrec.p, target - hitrec.p), objects)
  return sky(ray)

def color(ray, objects, depth):
  is_hit, hitrec = objects.hit(ray, 0.001, 9999999)
  if (is_hit):
    if (depth < 50):
      is_scatter, scattered, attenuation = hitrec.material.scatter(ray, hitrec)
      if (is_scatter):
        return attenuation * color(scattered, objects, depth + 1)
    return np.array([0.0, 0.0, 0.0])
  return sky(ray)

def draw_sphere():
  nx = 200
  ny = 100
  low_left_corner = np.array([-2.0, -1.0, -1.0])
  horizontal = np.array([4.0, 0.0, 0.0])
  vertical = np.array([0.0, 2.0, 0.0])
  origin = np.zeros(3, dtype=float)
  sphere = Sphere([0.0, 0.0, -1.0], 0.5)

  img_arr = []
  for j in range(ny-1, -1, -1):
    row = []
    for i in range(nx):
      u = float(i) / nx
      v = float(j) / ny
      ray = Ray(origin, low_left_corner + u * horizontal + v * vertical)
      col = color_s(ray, sphere)
      row.append([col[0] * 255.0, col[1] * 255.0, col[2] * 255.0])
    img_arr.append(row)

  img = Image.fromarray(np.uint8(np.array(img_arr)))
  img.show()

if __name__ == '__main__':
  start = time.time()
  nx = 200
  ny = 100
  ns = 100
  camera = Camera()
  sphere = Sphere([0.0, 0.0, -1.0], 0.5, Lambertian(np.array([0.8, 0.3, 0.3])))
  sphere2 = Sphere([0.0, -100.5, -1.0], 100.0, Lambertian(np.array([0.8, 0.8, 0.0])))
  sphere3 = Sphere([1.0, 0.0, -1.0], 0.5, Metal(np.array([0.8, 0.6, 0.2]), 1.0))
  sphere4 = Sphere([-1.0, 0.0, -1.0], 0.5, Metal(np.array([0.8, 0.8, 0.8]), 0.3))
  objects = ShapeList([sphere, sphere2, sphere3, sphere4])

  img_arr = []
  for j in range(ny-1, -1, -1):
    row = []
    for i in range(nx):
      col = np.array([0.0, 0.0, 0.0])
      for s in range(ns):
        u = (float(i) + random.uniform(0.0, 1.0)) / nx
        v = (float(j) + random.uniform(0.0, 1.0)) / ny
        ray = camera.getRay(u, v)
        col += color(ray, objects, 0)
      col /= ns 
      col = np.sqrt(col)
      row.append([col[0] * 255.0, col[1] * 255.0, col[2] * 255.0])
    img_arr.append(row)

  img = Image.fromarray(np.uint8(np.array(img_arr)))
  end = time.time()
  print(end - start)
  img.show()