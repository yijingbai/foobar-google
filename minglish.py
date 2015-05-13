# Minglish lesson
# ===============

# Welcome to the lab, minion. Henceforth you shall do the bidding of Professor Boolean. Some say he's mad, trying to develop a zombie serum and all... but we think he's brilliant! 

# First things first - Minions don't speak English, we speak Minglish. Use the Minglish dictionary to learn! The first thing you'll learn is how to use the dictionary.

# Open the dictionary. Read the page numbers, figure out which pages come before others. You recognize the same letters used in English, but the order of letters is completely different in Minglish than English (a < b < c < ...).

# Given a sorted list of dictionary words (you know they are sorted because you can read the page numbers), can you find the alphabetical order of the Minglish alphabet? For example, if the words were ["z", "yx", "yz"] the alphabetical order would be "xzy," which means x < z < y. The first two words tell you that z < y, and the last two words tell you that x < z.

# Write a function answer(words) which, given a list of words sorted alphabetically in the Minglish alphabet, outputs a string that contains each letter present in the list of words exactly once; the order of the letters in the output must follow the order of letters in the Minglish alphabet. 

# The list will contain at least 1 and no more than 50 words, and each word will consist of at least 1 and no more than 50 lowercase letters [a-z]. It is guaranteed that a total ordering can be developed from the input provided (i.e. given any two distinct letters, you can tell which is greater), and so the answer will exist and be unique.

# Languages
# =========

# To provide a Python solution, edit solution.py
# To provide a Java solution, edit solution.java

# Test cases
# ==========

# Inputs:
#     (string list) words = ["y", "z", "xy"]
# Output:
#     (string) "yzx"

# Inputs:
#     (string list) words = ["ba", "ab", "cb"]
# Output:
#     (string) "bac"

# Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.

# topological sort
# http://stackoverflow.com/questions/15038876/topological-sort-python

import collections
from itertools import groupby, takewhile, count

def answer(words):
    lesson = Minglish()
    res = lesson.run(words)
    return res

class Minglish(object):
    def __init__(self):
        self.blueprint = collections.defaultdict(set)
        return

    def run(self, words):
        self.buildbp(words)
        return ("".join(sort_topologically(self.blueprint)))[::-1]

    def buildbp(self, words):
        if not words:
            return
        heads = [key for key, group in groupby(words, lambda w: w[0])]
        for orig, dest in zip(heads[:-1], heads[1:]):
            self.blueprint[orig].add(dest)
        for key, group in groupby(words, lambda w: w[0]):
            g = [s[1:] for s in group if s[1:]]
            if g:
                self.buildbp(g)

def sort_topologically(graph):
    levels_by_name = {}
    names_by_level = collections.defaultdict(set)

    def walk_depth_first(name):
        if name in levels_by_name:
            return levels_by_name[name]
        children = graph.get(name, None)
        level = 0 if not children else (1 + max(walk_depth_first(lname) for lname in children))
        levels_by_name[name] = level
        names_by_level[level].add(name)
        return level

    for name in graph:
        walk_depth_first(name)

    return flatten(list(takewhile(lambda x: x is not None, (names_by_level.get(i, None) for i in count()))))

def flatten(listoflist):
    return [item for sub in listoflist for item in sub]


def test(words, truth):
    res = answer(words)
    print truth == res, " ** ", truth, " -- ", res
def tests():
    test(["y", "z", "xy"], "yzx")
    test(["ba", "ab", "cb"], "bac")
    test(["a", "ba"], "ab")
    # test(["abc", "abd", "bak", "baz", "cbb"], "some")

tests()