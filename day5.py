import sys
import datetime
import re

# Set input data file
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "input5.txt"
input_data = open(filename, "r").read()
alphabet = "abcdefghijklmnopqrstuvwxyz"

print "Original len: %d" % len(input_data)

min_len = len(input_data)
min_char = ""
for char in alphabet:
    input_c = input_data.replace(char, "").replace(char.upper(), "")
    c_pointer = 0
    next_pointer = 1
    history = []
    while next_pointer < len(input_c):
        current_c = input_c[c_pointer]
        next_c = input_c[next_pointer]
        if current_c != next_c and current_c.upper() == next_c.upper():
            if len(history) > 0:
                c_pointer = history[-1]
                history = history [:-1]
                next_pointer += 1
            else:
                c_pointer = next_pointer+1
                next_pointer += 2
        else:
            history += [c_pointer]
            c_pointer = next_pointer
            next_pointer += 1
    if len(history) < min_len:
        min_len = len(history)
        min_char = char

print "Minimum length is %d (filtered %s)" % (min_len, min_char)

