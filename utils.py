import numpy as np
import random

def lengthSqr(arr):
  return np.sum(arr * arr)

def length(arr):
  return (np.sqrt(np.sum(arr * arr)))

def unit_vector(arr):
  return arr / length(arr)

def random_in_unit():
  p = np.array([0.0, 0.0, 0.0])
  while (lengthSqr(p) < 1.0):
    p = 2.0 * np.array([random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)]) - np.array([1.0, 1.0, 1.0])
  return p

def reflect(vec, normal):
  return vec - 2 * np.dot(vec, normal) * normal