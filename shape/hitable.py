class Hitable(object):
  def __init__(self):
    pass

  def hit(self, ray, t_min, t_max):
    return True, None