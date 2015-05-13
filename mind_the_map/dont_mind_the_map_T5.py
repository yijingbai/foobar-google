
# ============= Util helpers ==================
def step(subway, station_from, direction, skipper):
  station_to = subway[station_from][direction]
  if skipper == station_to:
    station_to = subway[station_to][direction]
  if skipper == station_to:
    station_to = station_from
  return station_to

def keep_short_squash(paths):
  '''when pony is prefix of horse, keep pony only'''
  paths.sort(key = len, reverse = True)
  ps = paths[:]
  for horse in xrange(len(paths)-1):
    for pony in xrange(horse+1, len(paths)):
      if paths[horse].startswith(paths[pony]):
        ps.remove(paths[horse])
        break
  return ps

def _pick_long(path1, path2):
  if path1 == path2 or path1.startswith(path2):
    return path1
  elif path2.startswith(path1):
    return path2
  else:
    return None

def keep_long_intersection(paths1, paths2):
  '''when pony is prefix of horse, keep horse only'''
  '''similar to set & set, but the rule expands to prefix'''
  ps = []
  for p1 in paths1:
    for p2 in paths2:
      picked = _pick_long(p1, p2)
      if picked and picked not in ps:
        ps.append(picked)
  return ps

# =========== Weight lifters ============

class Bicycle(object):
  '''Dealing with 2 rabbits'''
  def __init__(self, subway):
    self.subway = subway
    self.direction_max = len(subway[0])

  def _recursive_get_paths(self, s1, s2, path, skipper):
    for direction in xrange(self.direction_max):
      next1 = step(self.subway, s1, direction, skipper)
      next2 = step(self.subway, s2, direction, skipper)
      if next1 == next2: # order matters?
        path.append(direction)
        self.paths.append('-'.join(map(str, path)) )
        path.pop()
        continue
      if (next1, next2) in self.bike_shed:
        continue
      self.bike_shed.add((next1, next2))
      path.append(direction)
      self._recursive_get_paths(next1, next2, path, skipper)
      path.pop()

  def good_paths(self, s1, s2, skipper):
    self.paths = []
    self.bike_shed = set()
    self._recursive_get_paths(s1, s2, [], skipper)
    return keep_short_squash(self.paths)

class GoodMuni(object):
  def __init__(self, subway):
    self.subway = subway
    self.bike = Bicycle(subway)
    self.station_max = len(subway)
    self.direction_max = len(subway[0])

  def drive(self):
    if self.station_max == 1:
      return -1
    skipper = None
    s1, s2 = 0, 1
    first_path = self.bike.good_paths(s1, s2, skipper)
    if not first_path:
      if self.station_max == 2:
        return 0
      else:
        return -3
    for s2 in xrange(2, self.station_max):
      s1 = s2 - 1
      next_path = self.bike.good_paths(s1, s2, skipper)
      final_paths = keep_long_intersection(first_path, next_path)
      if not final_paths:
        return -3
      first_path = next_path
    return -1

import itertools
class BadMuni(object):
  def __init__(self, subway):
    self.subway = subway
    self.bike = Bicycle(subway)
    self.station_max = len(subway) # >= 3
    self.direction_max = len(subway[0])

  def drive(self):
    for skipper in xrange(self.station_max):
      stations = range(skipper)
      stations.extend(range(skipper + 1, self.station_max))
      s1, s2 = stations[0], stations[1]
      first_path = self.bike.good_paths(s1, s2, skipper)
      if not first_path:
        continue
      for index in xrange(2, self.station_max-1):
        s1, s2 = stations[index-1], stations[index]
        next_path = self.bike.good_paths(s1, s2, skipper)
        final_paths = keep_long_intersection(first_path, next_path)
        if not final_paths:
          break
        first_path = next_path
      else:
        return skipper
    return -2

def answer(subway):
  m = GoodMuni(subway)
  good_res = m.drive()
  if good_res == -3:
    badm = BadMuni(subway)
    return badm.drive()
  return good_res

# ============= Tests ===========
def pprint(value, truth):
  print value == truth, value, truth

def biketests():
  subway = [[2, 1], [2, 0], [3, 1], [1, 0]]
  bike = Bicycle(subway)
  print bike.good_paths(0, 1, None)
  print bike.good_paths(1, 2, None)
  print bike.good_paths(2, 3, None)
  print bike.good_paths(3, 0, None)

def goodmunitest(subway, truth):
  m = GoodMuni(subway)
  value = m.drive()
  pprint(value, truth)

def goodmunitests():
  goodmunitest(subway = [[1], [0]], truth = 0)
  goodmunitest(subway = [[2, 1], [2, 0], [3, 1], [1, 0]], truth = -1)
  goodmunitest(subway = [[1, 2], [1, 1], [2, 2]], truth = 1)

def answertest(subway, truth):
  value = answer(subway)
  pprint(value, truth)

def answertests():
  answertest(subway = [[1], [0]], truth = 0)
  answertest(subway = [[2, 1], [2, 0], [3, 1], [1, 0]], truth = -1)
  answertest(subway = [[1, 2], [1, 1], [2, 2]], truth = 1)

def tests():
  # biketests()
  # goodmunitests()
  answertests()
  return

tests()