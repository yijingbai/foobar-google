# String cleaning
# ===============

# Your spy, Beta Rabbit, has managed to infiltrate a lab of mad scientists who are turning rabbits into zombies. He sends a text transmission to you, but it is intercepted by a pirate, who jumbles the message by repeatedly inserting the same word into the text some number of times. At each step, he might have inserted the word anywhere, including at the beginning or end, or even into a copy of the word he inserted in a previous step. By offering the pirate a dubloon, you get him to tell you what that word was. A few bottles of rum later, he also tells you that the original text was the shortest possible string formed by repeated removals of that word, and that the text was actually the lexicographically earliest string from all the possible shortest candidates. Using this information, can you work out what message your spy originally sent?

# For example, if the final chunk of text was "lolol," and the inserted word was "lol," the shortest possible strings are "ol" (remove "lol" from the beginning) and "lo" (remove "lol" from the end). The original text therefore must have been "lo," the lexicographically earliest string.

# Write a function called answer(chunk, word) that returns the shortest, lexicographically earliest string that can be formed by removing occurrences of word from chunk. Keep in mind that the occurrences may be nested, and that removing one occurrence might result in another. For example, removing "ab" from "aabb" results in another "ab" that was not originally present. Also keep in mind that your spy's original message might have been an empty string.

# chunk and word will only consist of lowercase letters [a-z].
# chunk will have no more than 20 characters.
# word will have at least one character, and no more than the number of characters in chunk.

# Languages
# =========

# To provide a Python solution, edit solution.py
# To provide a Java solution, edit solution.java

# Test cases
# ==========

# Inputs:
#     (string) chunk = "lololololo"
#     (string) word = "lol"
# Output:
#     (string) "looo"

# Inputs:
#     (string) chunk = "goodgooogoogfogoood"
#     (string) word = "goo"
# Output:
#     (string) "dogfood"

# Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.
import re

def answer(chunk, word):
    chunk = [chunk]
    while(chunk):
        res = set(chunk)
        chunk = flatten(auto_shrinkall(word, res))
    return min(res)

# return the starts position of all matches, overlap allowed
def findall(word, chunk):
    needle = re.compile("(?=" + word + ")")
    starts = re.finditer(needle, chunk)
    return [p.span()[0] for p in starts]

def shrink(start, length, str):
    return str[:start] + str[start+length:]

def shrinkall(starts, length, str):
    return [shrink(start, length, str) for start in starts]

def auto_shrinkall(word, chunk_set):
    return [shrinkall(findall(word, chunk), len(word), chunk) for chunk in chunk_set]

def flatten(listoflist):
    return [item for sub in listoflist for item in sub]

def test():
    chunk = "lololololo"
    word = "lol"
    starts = findall(word, chunk)
    print starts
    print shrinkall(starts, len(word), chunk)
    res = "looo"
    a = answer(chunk, word)
    print a, a == res

    chunk = "goodgooogoogfogoood"
    word = "goo"
    res = "dogfood"
    a = answer(chunk, word)
    print a, a == res
    print auto_shrinkall(word, set([chunk]))

    chunk_set = ["abcd", "bbc"]
    word = "ab"
    print auto_shrinkall(word, chunk_set)
    print flatten(auto_shrinkall(word, chunk_set))

test()


