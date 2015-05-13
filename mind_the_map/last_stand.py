# ============= Util helpers ==================
def step(subway, station_from, direction, skipper):
  station_to = subway[station_from][direction]
  if skipper == station_to:
    station_to = subway[station_to][direction]
  if skipper == station_to:
    station_to = station_from
  return station_to

def group_step(subway, stations_from, direction, skipper):
  return frozenset([step(subway, station, direction, skipper) for station in stations_from])

def follow(subway, station, directions, skipper):
  '''Where the directions lead to, given the station to start with'''
  for direction in directions:
    station = step(subway, station, direction, skipper)
  return station

def group_follow(subway, stations_from, directions, skipper):
  return frozenset([follow(subway, station, directions, skipper) for station in stations_from])

def keep_short_squash(instructions):
  '''when pony is prefix of horse, keep pony only'''
  instructions.sort(key = len, reverse = True)
  ps = instructions[:]
  for horse in xrange(len(instructions)-1):
    for pony in xrange(horse+1, len(instructions)):
      if instructions[horse].startswith(instructions[pony]):
        ps.remove(instructions[horse])
        break
  return ps

def squash(directions):
  dirs = []
  for ins in directions:
    if ins:
      dirs.append('-'.join(map(str, ins)) )

  res = []
  for line in dirs:
    ins = map(lambda n: int(n), line.split('-'))
    res.append(ins)
  return res

# =========== Weight lifters ============

class Jeep(object):
  '''Dealing with 5 rabbits, construct the initial instructions to test on'''
  def __init__(self, subway):
    self.subway = subway
    self.direction_max = len(subway[0])

  def _recursive_get_instructions(self, stations, current_instruction, skipper):
    for direction in xrange(self.direction_max):
      stations_next = group_step(self.subway, stations, direction, skipper)
      if len(stations_next) == 1: # converged
        current_instruction.append(direction)
        self.instructions.append('-'.join(map(str, current_instruction)) )
        current_instruction.pop()
        continue
      if stations_next in self.yard:
        continue
      self.yard.add(stations_next)
      current_instruction.append(direction)
      self._recursive_get_instructions(stations_next, current_instruction, skipper)
      current_instruction.pop()

  def candy_instructions(self, stations, skipper):
    self.instructions = []
    self.yard = set()
    self._recursive_get_instructions(stations, [], skipper)
    return keep_short_squash(self.instructions)

  def step_instructions(self, stations, skipper):
    candy = self.candy_instructions(stations, skipper)
    res = []
    for line in candy:
      ins = map(lambda n: int(n), line.split('-'))
      res.append(ins)
    return res

def launch(subway):
  if len(subway) <= 5:
    return simple_launch(subway)
  else:
    return complex_launch(subway)


def simple_launch(subway):
  '''For less than 5 stations '''
  jeep = Jeep(subway)
  if len(subway) == 1:
    return -1
  for skipper in xrange(-1, len(subway)):
    stations = range(skipper)
    stations.extend(range(skipper + 1, len(subway)))
    directions = jeep.candy_instructions(stations, skipper)
    if directions:
      return skipper
  return -2

import itertools
def complex_launch(subway):
  '''For more than 5 stations '''
  jeep = Jeep(subway)
  for skipper in xrange(-1, len(subway)):
    stations_all = range(skipper)
    stations_all.extend(range(skipper + 1, len(subway)))
    sample_index = len(stations_all) - 3 - len(stations_all) % 3
    stations_header = stations_all[sample_index:]
    stations_body = stations_all[:sample_index]
    sample_direction_groups = jeep.step_instructions(stations_header, skipper)
    station_groups = itertools.groupby(stations_body, lambda ss: ss / 3)
    for k, sgroup in station_groups:
      stations_from = list(sgroup)
      for sample_directions in sample_direction_groups:
        if not sample_directions:
          continue
        stations_destination = group_follow(subway, stations_from, sample_directions, skipper)
        if len(stations_destination) == 1:
          continue
        else:
          addition_directions = jeep.step_instructions(stations_destination, skipper)
          if addition_directions:
            for append_list in addition_directions:
              prefix_copy = sample_directions[:]
              add_dir_list = prefix_copy.extend(append_list)
              sample_direction_groups.append(add_dir_list)
            sample_direction_groups = squash(sample_direction_groups)
            continue
          else:
            sample_direction_groups.remove(sample_directions)
      if not sample_direction_groups:
        break
    else:
      return skipper
  return -2


def answer(subway):
  return launch(subway)

# ============= Tests ===========
def pprint(value, truth):
  print value == truth, value, truth

def launchertest(subway, truth):
  v = complex_launch(subway)
  pprint(v, truth)

def tests():
  launchertest(subway = [[1], [0]], truth = 0)
  launchertest(subway = [[2, 1], [2, 0], [3, 1], [1, 0]], truth = -1)
  launchertest(subway = [[1, 2], [1, 1], [2, 2]], truth = 1)
  arbit = [[2,4,6,1],[1,6,0,2],[7,2,8,5],[4,2,6,5],[7,6,5,4],[1,2,3,4],[9,8,1,4],[1,6,3,7],[1,6,4,7],[1,6,4,7]]
  launchertest(arbit, 1)
  return

tests()
