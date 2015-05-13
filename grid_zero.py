# foobar:~/ USER$ request
# Requesting challenge...
# New challenge "grid_zero" added to your home folder.
# Time to solve: 192 hours.
# foobar:~/ USER$ ls
# grid_zero
# start_here.txt
# foobar:~/ USER$ cd grid_zero/
# foobar:~/grid_zero USER$ cat readme.txt 
# Grid Zero
# =========

# You are almost there. The only thing between you and foiling Professor Boolean's plans for good is a square grid of lights, only some of which seem to be lit up. The grid seems to be a lock of some kind. That's interesting. Touching a light toggles the light, as well as all of the other lights in the same row and column as that light. 

# Wait! The minions are coming - better hide. 

# Yes! By observing the minions, you see that the light grid is, indeed, a lock. The key is to turn off all the lights by touching some of them. The minions are gone now, but the grid of lights is now lit up differently. Better unlock it fast, before you get caught.

# The grid is always a square. You can think of the grid as an NxN matrix of zeroes and ones, where one denotes that the light is on, and zero means that the light is off.

# For example, if the matrix was

# 1 1
# 0 0

# Touching the bottom left light results in

# 0 1
# 1 1

# Now touching the bottom right light results in

# 0 0
# 0 0

# ...which unlocks the door.

# Write a function answer(matrix) which returns the minimum number of lights that need to be touched to unlock the lock, by turning off all the lights. If it is not possible to do so, return -1. 

# The given matrix will be a list of N lists, each with N elements. Element matrix[i][j] represents the element in row i, column j of the matrix. Each element will be either 0 or 1, 0 representing a light that is off, and 1 representing a light that is on. 

# N will be a positive integer, at least 2 and no more than 15.


# Languages
# =========

# To provide a Python solution, edit solution.py
# To provide a Java solution, edit solution.java

# Test cases
# ==========

# Inputs:
#     (int) matrix = [[1, 1], [0, 0]]
# Output:
#     (int) 2

# Inputs:
#     (int) matrix = [[1, 1, 1], [1, 0, 0], [1, 0, 1]]
# Output:
#     (int) -1

# Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.

# Use bottom-left corner as origin, to comply with position order of binary digits

def rc2pos(row, col, dim):
  '''(row, col) to linear position'''
  return row * dim + col

def pos2rc(pos, dim):
  '''linear position to (row, col)'''
  row = pos // dim
  col = pos % dim
  return (row, col)

def rotate(bnum, dim):
  '''Left rotate a matrix, which is represented by the binary array of bnum.'''
  res = 0
  for pos in xrange(dim * dim):
    if not bnum:
      return res # short-cut
    dig = bnum & 1
    bnum >>= 1
    if not dig:
      continue # short-cut
    row, col = pos2rc(pos, dim)
    col_r = row
    row_r = dim - 1 - col
    pos_r = rc2pos(row_r, col_r, dim)
    res += 1 << pos_r
  return res

def mirror(bnum, dim):
  '''The mirror is horizontal, as mirror-pond'''
  res = 0
  for pos in xrange(dim * dim):
    if not bnum:
      return res # short-cut
    dig = bnum & 1
    bnum >>= 1
    if not dig:
      continue # short-cut
    row, col = pos2rc(pos, dim)
    col_r = col
    row_r = dim - 1 - row
    pos_r = rc2pos(row_r, col_r, dim)
    res += 1 << pos_r
  return res

def congruence(bnum, dim):
  '''8 congruence numbers, then de-dup'''
  res = [bnum, mirror(bnum, dim)]
  for ii in xrange(4):
    bnum = rotate(bnum, dim)
    m = mirror(bnum, dim)
    res.append(bnum)
    res.append(m)
  return set(res)

def flip(bnum, pos, dim):
  row, col = pos2rc(pos, dim)
  row_pos = [rc2pos(row, ii, dim) for ii in range(dim)]
  col_pos = [rc2pos(ii, col, dim) for ii in range(dim)]
  row_mask = sum([1<<x for x in row_pos])
  col_mask = sum([1<<x for x in col_pos])
  double_count_mask = 1 << pos
  res = bnum ^ row_mask ^ col_mask ^ double_count_mask
  return res

def answer(matrix):
    # your code here
    dim = len(matrix)
    bnum_str = ''.join([''.join(map(str, r)) for r in matrix])
    bnum = int(bnum_str, 2)
    bnum_set = congruence(bnum, dim)

    level = 0
    full_set = set([0])
    prev_set = set([0])
    while True:
      level += 1
      curr_set = set()
      for seed in prev_set:
        for ii in xrange(dim * dim): # optimization for symmetry?
          flipped = flip(seed, ii, dim)
          if flipped in bnum_set:
            return level
          if flipped in full_set:
            continue
          else:
            curr_set |= congruence(flipped, dim)
      if curr_set <= full_set:
        return -1
      full_set |= curr_set
      prev_set = curr_set
    return -1


# =========== Tests ====================

def pos_tests():
  dim = 3
  row = 1
  col = 2
  pos = 5
  assert rc2pos(row, col, dim) == pos
  assert pos2rc(pos, dim) == (row, col)

def rotate_and_mirror_tests():
  dim = 3
  v = 3 # 000 000 011
  m = 192 # 011 000 000
  r1 = 72 # 001 001 000
  m1 = 9 # 000 001 001
  r2 = 384 # 110 000 000
  m2 = 6 # 000 000 110
  r3 = 36 # 000 100 100
  m3 = 288 # 100 100 000

  mir0 = mirror(v, dim)
  assert mir0 == m

  rot1 = rotate(v, dim)
  assert rot1 == r1

  mir1 = mirror(r1, dim)
  assert mir1 == m1

  rot2 = rotate(r1, dim)
  assert rot2 == r2

  mir2 = mirror(r2, dim)
  assert mir2 == m2

  rot3 = rotate(r2, dim)
  assert rot3 == r3

  mir3 = mirror(r3, dim)
  assert mir3 == m3

def congruence_tests():
  dim = 3
  v = 3
  con = [3, 192, 72, 9, 384, 6, 36, 288]
  assert congruence(v, dim) == set(con)

def flip_tests():
  dim = 3
  v = 3
  pos = 0
  fv = 76 # 001 001 100
  assert flip(v, pos, dim) == fv

def answer_tests():
  matrix = [[1, 1], [0, 0]]
  assert answer(matrix) == 2
  matrix = [[1, 1, 1], [1, 0, 0], [1, 0, 1]]
  assert answer(matrix) == -1

def tests():
  pos_tests()
  rotate_and_mirror_tests()
  flip_tests()
  congruence_tests()
  answer_tests()

tests()
