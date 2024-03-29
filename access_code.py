# foobar:~/access_codes USER$ cat readme.txt 
# Access codes
# ============

# You've discovered the evil laboratory of Dr. Boolean, and you've found that the vile doctor is transforming your fellow rabbit kin into terrifying rabbit-zombies! Naturally, you're less-than-happy about this turn of events.

# Of course where there's a will, there's a way. Your top-notch assistant, Beta Rabbit, managed to sneak in and steal some access codes for Dr. Boolean's lab in the hopes that the two of you could then return and rescue some of the undead rabbits. Unfortunately, once an access code is used it cannot be used again. Worse still, if an access code is used, then that code backwards won't work either! Who wrote this security system?

# Your job is to compare a list of the access codes and find the number of distinct codes, where two codes are considered to be "identical" (not distinct) if they're exactly the same, or the same but reversed. The access codes only contain the letters a-z, are all lowercase, and have at most 10 characters. Each set of access codes provided will have at most 5000 codes in them.

# For example, the access code "abc" is identical to "cba" as well as "abc." The code "cba" is identical to "abc" as well as "cba." The list ["abc," "cba," "bac"] has 2 distinct access codes in it.

# Write a function answer(x) which takes a list of access code strings, x, and returns the number of distinct access code strings using this definition of identical.

# Languages
# =========

# To provide a Python solution, edit solution.py
# To provide a Java solution, edit solution.java

# Test cases
# ==========

# Inputs:
#     (string list) x = ["foo", "bar", "oof", "bar"]
# Output:
#     (int) 2

# Inputs:
#     (string list) x = ["x", "y", "xy", "yy", "", "yx"]
# Output:
#     (int) 5

# Use verify [file] to test your solution and see how it does. When you are finished editing your code, use submit [file] to submit your answer. If your solution passes the test cases, it will be removed from your home folder.
# foobar:~/access_codes USER$ ls
# readme.txt
# constraints.txt
# solution.py
# solution.java
# foobar:~/access_codes USER$ cat constraints.txt 
# Java
# ====

# Your code will be compiled using standard Java 7. It must implement the answer() method in the solution stub.

# Execution time is limited. Some classes are restricted (e.g. java.lang.ClassLoader). You will see a notice if you use a restricted class when you verify your solution.

# Third-party libraries, input/output operations, spawning threads or processes and changes to the execution environment are not allowed.

# Python
# ======

# Your code will run inside a Python 2.7.6 sandbox.

# Standard libraries are supported except for bz2, crypt, fcntl, mmap, pwd, pyexpat, select, signal, termios, thread, time, unicodedata, zipimport, zlib.

def answer(x):
    keeper = set()
    for s in x:
        if s not in keeper and s[::-1] not in keeper:
            keeper.add(s)
    return len(keeper)

# Invite a friend to try a challenge. Send link below. It will only work once.
# https://goo.gl/Sl3xaX

def test():
    x1 = ["foo", "bar", "oof", "bar"]
    x2 = ["x", "y", "xy", "yy", "", "yx"]
    print answer(x1)
    print answer(x2)
    print answer(x1) == 2
    print answer(x2) == 5
