# foobar:~/ USER$ request
# Requesting challenge...
# New challenge "binary_bunnies" added to your home folder.
# Time to solve: 144 hours.
# foobar:~/ USER$ ls
# binary_bunnies
# start_here.txt
# foobar:~/ USER$ cd binary_bunnies/
# foobar:~/binary_bunnies USER$ cat readme.txt 
# Binary bunnies
# ==============

# As more and more rabbits were rescued from Professor Booleans horrid laboratory, you had to develop a system to track them, since some habitually continue to gnaw on the heads of their brethren and need extra supervision. For obvious reasons, you based your rabbit survivor tracking system on a binary search tree, but all of a sudden that decision has come back to haunt you.

# To make your binary tree, the rabbits were sorted by their ages (in days) and each, luckily enough, had a distinct age. For a given group, the first rabbit became the root, and then the next one (taken in order of rescue) was added, older ages to the left and younger to the right. The order that the rabbits returned to you determined the end pattern of the tree, and herein lies the problem.

# Some rabbits were rescued from multiple cages in a single rescue operation, and you need to make sure that all of the modifications or pathogens introduced by Professor Boolean are contained properly. Since the tree did not preserve the order of rescue, it falls to you to figure out how many different sequences of rabbits could have produced an identical tree to your sample sequence, so you can keep all the rescued rabbits safe.

# For example, if the rabbits were processed in order from [5, 9, 8, 2, 1], it would result in a binary tree identical to one created from [5, 2, 9, 1, 8]. 

# You must write a function answer(seq) that takes an array of up to 50 integers and returns a string representing the number (in base-10) of sequences that would result in the same tree as the given sequence.

# Languages
# =========

# To provide a Python solution, edit solution.py
# To provide a Java solution, edit solution.java

# Test cases
# ==========

# Inputs:
#     (int list) seq = [5, 9, 8, 2, 1]
# Output:
#     (string) "6"

# Inputs:
#     (int list) seq = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# Output:
#     (string) "1"

# Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.
def answer(seq):
  root = build_tree(seq)
  res = calc(root)
  return res


def comb(m, n):
  '''Choose m from n'''
  if m == n: # case (0, 0) included
    return 1
  if m > n:
    return 0
  if m > n/2: # compiler should optimze n/2 with bit shift. or use 2*m > n (earlier overflow?)
    m = n - m # simple optimization

  res = 1
  for ii in xrange(m):
    kid = n - ii 
    mom = ii + 1
    res = res * kid / mom
  return res

class Node(object):
  def __init__(self, value):
    self.value = value
    self.left = None
    self.right =None
    self.count = 1 # self

# return a root node ref
def build_tree(values):
  root = Node(values[0])
  for v in values[1:]:
    insert(root, v)
  return root

def insert(root, value):
  n = Node(value)
  _insert(root, n)
  return

# resursive method
def _insert(root, node):
  root.count += 1
  if node.value < root.value:
    if root.left:
      _insert(root.left, node)
    else:
      root.left = node
  else:
    if root.right:
      _insert(root.right, node)
    else:
      root.right = node
  return

def calc(root):
  if not root.left and not root.right:
    return 1
  if not root.left:
    return calc(root.right)
  if not root.right:
    return calc(root.left)
  cc = comb(root.left.count, root.count - 1)
  return cc * calc(root.left) * calc(root.right)

def tests():
  s1 = [5, 9, 8, 2, 1]
  a1 = answer(s1)
  r1 = 6
  print r1, r1 == a1, a1

  s1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  a1 = answer(s1)
  r1 = 1
  print r1, r1 == a1, a1

tests()


# foobar:~/binary_bunnies USER$ edit solution.py
# foobar:~/binary_bunnies USER$ verify solution.py
# Verifying solution...
# All test cases passed.
# foobar:~/binary_bunnies USER$ submit solution.py
# Are you sure you want to submit your solution?
# [Y]es or [N]o: Y
# Submitting solution...
# Submission: SUCCESSFUL. Completed in: 20 hrs, 41 mins, 28 secs.

# Current level: 4. Challenges to complete level: 2.  

# Level 1 100% [==========================================]
# Level 2 100% [==========================================]
# Level 3 100% [==========================================]
# Level 4  50% [=====================.....................]
# Level 5   0% [..........................................]

# Type request to request a new challenge now, or come back later.
# [#1] The code is strong with this one. Share solutions with a Google recruiter? 
# [Y]es [N]o [A]sk me later: A
# Response: contact postponed.
# To share your progress at any time, use the recruitme command.