class Ray:
  def __init__(self, ori, dir):
    self.origin = ori
    self.direction = dir

  def at(self, t):
    return self.origin + t * self.direction
