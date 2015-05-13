# foobar:~/line_up_the_captives USER$ cat readme.txt 
# Line up the captives
# ====================

# As you ponder sneaky strategies for assisting with the great rabbit escape, you realize that you have an opportunity to fool Professor Booleans guards into thinking there are fewer rabbits total than there actually are.

# By cleverly lining up the rabbits of different heights, you can obscure the sudden departure of some of the captives.

# Beta Rabbits statisticians have asked you for some numerical analysis of how this could be done so that they can explore the best options.

# Luckily, every rabbit has a slightly different height, and the guards are lazy and few in number. Only one guard is stationed at each end of the rabbit line-up as they survey their captive population. With a bit of misinformation added to the facility roster, you can make the guards think there are different numbers of rabbits in holding.

# To help plan this caper you need to calculate how many ways the rabbits can be lined up such that a viewer on one end sees x rabbits, and a viewer on the other end sees y rabbits, because some taller rabbits block the view of the shorter ones.

# For example, if the rabbits were arranged in line with heights 30 cm, 10 cm, 50 cm, 40 cm, and then 20 cm, a guard looking from the left side would see 2 rabbits (30 and 50 cm) while a guard looking from the right side would see 3 rabbits (20, 40 and 50 cm). 

# Write a method answer(x,y,n) which returns the number of possible ways to arrange n rabbits of unique heights along an east to west line, so that only x are visible from the west, and only y are visible from the east. The return value must be a string representing the number in base 10.

# If there is no possible arrangement, return "0".

# The number of rabbits (n) will be as small as 3 or as large as 40
# The viewable rabbits from either side (x and y) will be as small as 1 and as large as the total number of rabbits (n).

# Languages
# =========

# To provide a Python solution, edit solution.py
# To provide a Java solution, edit solution.java

# Test cases
# ==========

# Inputs:
#     (int) x = 2
#     (int) y = 2
#     (int) n = 3
# Output:
#     (string) "2"

# Inputs:
#     (int) x = 1
#     (int) y = 2
#     (int) n = 6
# Output:
#     (string) "24"

# Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.

# (x, y, n) => answer

# (1, 1, 1) => 1, while others (*, *, 1) => 0
# (1, 2, 2) => 1
# (2, 1, 2) => 1 (symmetric)


def answer(x, y, n):
  res = 0
  for ii in xrange(n):
    leftchoose = comb(ii, n - 1)
    leftview = sideview(x - 1, ii)
    rightview = sideview(y - 1, n - ii - 1)
    res += leftchoose * leftview * rightview
  return str(res)

viewkeeper = dict()
factkeeper = dict()
permkeeper = dict()
combkeeper = dict()

def fact(n):
  if n in factkeeper:
    return factkeeper[n]
  res = n
  for ii in xrange(1, n):
    res *= ii
    factkeeper[n] = res
  return res

def perm(m, n):
  if (m, n) in permkeeper:
    return permkeeper[(m, n)]
  res = n
  for ii in xrange(n-m+1, n):
    res *= ii
  permkeeper[(m, n)] = res
  return res

def comb(m, n):
  '''Choose m from n'''
  if m == n: # case (0, 0) included
    return 1
  if m > n:
    return 0
  if m > n/2: # compiler should optimze n/2 with bit shift. or use 2*m > n (earlier overflow?)
    m = n - m # simple optimization

  if (m, n) in combkeeper:
    return combkeeper[(m, n)]
  res = 1
  for ii in xrange(m):
    kid = n - ii 
    mom = ii + 1
    res = res * kid / mom
  combkeeper[(m, n)] = res
  return res

def prettytest(value, truth, name = None):
  if value != truth:
    print False, value, " != ", truth, "  (%s)" % name

def permcombtests():
  k = "Factorial"
  prettytest(fact(2), 2, k)
  prettytest(fact(3), 6, k)
  prettytest(fact(5), 120, k)
  prettytest(fact(7), 5040, k)

  k = "Permuattions"
  prettytest(perm(1, 4), 4, k)
  prettytest(perm(2, 4), 12, k)
  prettytest(perm(2, 7), 42, k)
  prettytest(perm(5, 7), 2520, k)

  k = "Combination"
  prettytest(comb(1, 4), 4, k)
  prettytest(comb(2, 4), 6, k)
  prettytest(comb(2, 7), 21, k)
  prettytest(comb(5, 7), 21, k)

def sideview(x, n):
  if x == n:
    return 1
  if x > n:
    return 0
  if (x, n) in viewkeeper:
    return viewkeeper[(x, n)]
  res = 0
  for ii in xrange(n):
    leftchoose = comb(ii, n - 1)
    leftview = sideview(x - 1, ii)
    rightview = fact(n - ii - 1)
    res += leftchoose * leftview * rightview
  viewkeeper[(x, n)] = res
  return res

def sideviewtests():
  k = "sideview"
  prettytest(sideview(1, 1), 1, k)
  prettytest(sideview(1, 2), 1, k)
  prettytest(sideview(1, 3), 2, k)
  prettytest(sideview(2, 3), 2, k)


def answertests():
  k = "answer"
  prettytest(answer(2, 2, 3), "2", k)
  prettytest(answer(1, 2, 6), "24", k)

def alltests():
  permcombtests()
  sideviewtests()
  answertests()  

  print "All tests done."



alltests()