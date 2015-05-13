# foobar:~/undercover_underground USER$ cat readme.txt 
# Undercover underground
# ======================

# As you help the rabbits establish more and more resistance groups to fight against Professor Boolean, you need a way to pass messages back and forth.

# Luckily there are abandoned tunnels between the warrens of the rabbits, and you need to find the best way to use them. In some cases, Beta Rabbit wants a high level of interconnectedness, especially when the groups show their loyalty and worthiness. In other scenarios the groups should be less intertwined, in case any are compromised by enemy agents or zombits.

# Every warren must be connected to every other warren somehow, and no two warrens should ever have more than one tunnel between them. Your assignment: count the number of ways to connect the resistance warrens.

# For example, with 3 warrens (denoted A, B, C) and 2 tunnels, there are three distinct ways to connect them:

# A-B-C
# A-C-B
# C-A-B

# With 4 warrens and 6 tunnels, the only way to connect them is to connect each warren to every other warren.

# Write a function answer(N, K) which returns the number of ways to connect N distinctly labelled warrens with exactly K tunnels, so that there is a path between any two warrens. 

# The return value must be a string representation of the total number of ways to do so, in base 10.
# N will be at least 2 and at most 20. 
# K will be at least one less than N and at most (N * (N - 1)) / 2

# Languages
# =========

# To provide a Python solution, edit solution.py
# To provide a Java solution, edit solution.java

# Test cases
# ==========

# Inputs:
#     (int) N = 2
#     (int) K = 1
# Output:
#     (string) "1"

# Inputs:
#     (int) N = 4
#     (int) K = 3
# Output:
#     (string) "16"

# Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.
import logging
FORMAT = '%(funcName)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)

# def answer(N, K):
#     return connected(N, K)

# =======================

def answer(N, K):
  return q(N, K)

keeper = dict()
def q(n, k):
  if k < n -1 or k > n*(n-1) / 2:
    return 0
  if k == n - 1:
    if n == 1 or n == 2:
      return 1L
    return n ** (n -2)
  if (n, k) in keeper:
    return keeper[(n, k)]
  full_choices = choose(k,  n*(n-1) / 2) # max possible combinations with (n, k) without considering connectness
  to_exclude = sum([choose(m, n-1) * subq(n, k, m) for m in range(n-1)])
  res = full_choices - to_exclude
  keeper[(n, k)] = res
  return res

exkeeper = dict()
def exq(n, k):
  if (n, k) in exkeeper:
    return exkeeper[(n, k)]
  res = sum([choose(m, n-1) * subq(n, k, m) for m in range(n-1)])
  exkeeper[(n, k)] = res
  return res

subkeeper = dict()
def subq(n, k, m):
  if (n, k, m) in subkeeper:
    return subkeeper[(n, k, m)]
  res = sum([choose(p, (n-1-m)*(n-2-m)/2)* q(m+1, k-p) for p in range(k+1)])
  subkeeper[(n, k, m)] = res
  return res


cckeeper = dict()
def choose(m, n):
  '''Choose m from n'''
  if m == n: # case (0, 0) included
    return 1
  if m > n or n < 0 or m < 0:
    return 0
  if m > n/2: # compiler should optimze n/2 with bit shift. or use 2*m > n (earlier overflow?)
    m = n - m # simple optimization
  if (m, n) in cckeeper:
    return cckeeper[(m, n)]
  res = 1
  for ii in xrange(m):
    kid = n - ii 
    mom = ii + 1
    res = res * kid / mom
  cckeeper[(m, n)] = res
  return res

# hmm, time limit ...
# =======================

# foobar:~/undercover_underground USER$ verify solution.py
# Verifying solution...
# All test cases passed.
# foobar:~/undercover_underground USER$ submit solution.py
# Are you sure you want to submit your solution?
# [Y]es or [N]o: Y
# Submitting solution...
# Submission: SUCCESSFUL. Completed in: 1 day, 17 hrs, 47 mins, 18 secs.

# Level 4 complete. You are now on level 5. Challenges to complete level: 5.  

# Level 1 100% [==========================================]
# Level 2 100% [==========================================]
# Level 3 100% [==========================================]
# Level 4 100% [==========================================]
# Level 5   0% [..........................................]

# It's dangerous to go alone! Invite a friend to try a challenge. Send link below. It will only work once.
# https://goo.gl/hW8Vnm

# Type request to request a new challenge now, or come back later.
# [#1] The code is strong with this one. Share solutions with a Goo
# gle recruiter? 
# [Y]es [N]o [A]sk me later: A
# Response: contact postponed.
# To share your progress at any time, use the recruitme command.


def all_edges(n):
  '''Fully connected'''
  return n * (n-1) / 2

ckeeper = dict()
dckeeper = dict()

def connected(n, k):
  k_upper = all_edges(n)
  k_lower = n - 1
  if k < k_lower or k > k_upper:
    return 0
  if k == k_upper:
    return 1
  if (n, k) in ckeeper:
    return ckeeper[(n, k)]
  if k == k_lower:
    if k_lower == 1 or k_lower == 0:
      return 1
    res = n ** (n-2)
    ckeeper[(n, k)] = res
    return res
  full_choices = comb(k, k_upper) # max possible combinations with (n, k) without considering connectness
  to_exclude = disconnected(n, k)
  res = full_choices - to_exclude
  ckeeper[(n, k)] = res
  logger.debug("full_choices = %s, to_exclude = %s", full_choices, to_exclude)
  logger.debug("%s %s, res = %s", n, k, res)
  return res

def dis_edge_pick(n, k, n2, k2):
  '''Two groups are disjoint with constrains: (n1 + n2 == n) and (k1 + k2 == k)
  Group 1 (alias Scout) with n1 nodes is free style, do not have to be connected.
  Group 2 (alias Marine) with n2 nodes must be connected.
  Note: no edge-node upper- or lower-bound check for optimization as did in connected() so the caller should do the check.
  '''
  n1 = n - n2
  k1 = k - k2
  scout = comb(k1, all_edges(n1))
  marine = connected(n2, k2)
  res = scout * marine
  logger.debug("(%s %s), (%s %s), (%s %s), res = %s", n, k, n1, k1, n2, k2, res)
  logger.debug("scout = %s, marine = %s", scout, marine)
  return res

def dis_node_pick(n, k, n2):
  '''Fix node allocation, sum over ways to allocate edges between scout and marine
  '''
  res = 0
  for k2 in xrange(n2-1, k+1):
    res += comb(n2, n) * dis_edge_pick(n, k, n2, k2)
  logger.debug("%s %s %s, res = %s", n, k, n2, res)
  return res

def disconnected(n, k):
  '''Sum over ways to allocate nodes between scout and marine
  '''
  if (n, k) in dckeeper:
    return dckeeper[(n, k)]
  res = 0
  for n2 in xrange(2, n):
    res += comb(n2, n) * dis_node_pick(n, k, n2)
  dckeeper[(n, k)] = res
  logger.debug("%s %s, res = %s", n, k, res)
  return res

def comb(m, n):
  # if m > n:
  #   raise Exception("nono")
  res = choose(m, n)
  logger.debug("(%s, %s) ==> %s", m, n, res)
  return res

# ======================== Tests ==================

def test(n, k, truth):
  value = answer(n, k)
  print value == truth, n, k, value, truth

def group_tests():
  # http://math.stackexchange.com/questions/689526/how-many-connected-graphs-over-v-vertices-and-e-edges
  # the mothod above seems to be correct
  for index, truth in enumerate([1,1,3,16,125,1296,16807,262144,4782969,100000000]):
    n = index + 1
    k = n - 1
    test(n, k, truth)
  print ""
  print ""  
  for index, truth in enumerate([0,0,1,15,222,3660,68295,1436568,33779340,880107840]):
    n = index + 1
    k = n 
    test(n, k, truth)
  print ""
  print ""  
  for index, truth in enumerate([0,0,0,6,205,5700,156555,4483360,136368414,4432075200,154060613850]):
    n = index + 1
    k = n + 1
    test(n, k, truth)

def rabbit_tests():
  test(3, 2, 3)
  test(2, 1, 1)
  test(4, 3, 16)

def random_tests():
  test(5, 5, 222)
  test(6, 6, 3660)


def tests():
  # rabbit_tests()
  group_tests()
  # print ""
  # print ""

tests()