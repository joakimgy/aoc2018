import sys

# Set input data file
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "input16.txt"
input_data = open(filename, "r").readlines()

# Parse first section of input
print_n = 0
before, instructions, after = [], [], [] # part 1
test_program = []
for line in input_data:
    # Find
    if "Before" in line:
        b = line.split("[")[1][:-2]
        before += [map(int, b.split(","))]
        print_n = 3
    elif print_n == 0:
        test_program += [map(int, line.split())]
    else:
        print_n -= 1
        if "After" in line:
            a = line.split("[")[1][:-2]
            after += [map(int, a.split(","))]
        if print_n == 2:
            instructions += [map(int, line.split())]
test_program = test_program[2:]

##############
# Registers
r = {}
##############

##########################
# Operations
##########################
# Addition
def addr(a,b,c):
    r[c] = r[a]+r[b]
    return r[c]
def addi(a,b,c):
    r[c] = r[a]+b
    return r[c]
# Multiplication
def mulr(a,b,c):
    r[c] = r[a]*r[b]
    return r[c]
def muli(a,b,c):
    r[c] = r[a]*b
    return r[c]
# Bitwise AND
def banr(a,b,c):
    r[c] = r[a] & r[b]
    return r[c]
def bani(a,b,c):
    r[c] = r[a] & b
    return r[c]
# Bitwise OR:
def borr(a,b,c):
    r[c] = r[a] | r[b]
    return r[c]
def bori(a,b,c):
    r[c] = r[a] | b
    return r[c]
# Assignment
def setr(a,b,c):
    r[c] = r[a]
    return r[c]
def seti(a,b,c):
    r[c] = a
    return r[c]
# Greater-than testing
def gtir(a,b,c):
    r[c] = 1 if a>r[b] else 0
    return r[c]
def gtri(a,b,c):
    r[c] = 1 if r[a]>b else 0
    return r[c]
def gtrr(a,b,c):
    r[c] = 1 if r[a]>r[b] else 0
    return r[c]
# Equality testing
def eqir(a,b,c):
    r[c] = 1 if a==r[b] else 0
    return r[c]
def eqri(a,b,c):
    r[c] = 1 if r[a]==b else 0
    return r[c]
def eqrr(a,b,c):
    r[c] = 1 if r[a]==r[b] else 0
    return r[c]


##################
# Run the program
##################
functions = ([addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, 
            gtir, gtri, gtrr, eqir, eqri, eqrr])
# function[opcode] contains a counter of each program possible for that opcode
function = [[0 for _ in range(len(functions))] for _ in range(len(functions))]
# Part 1
samples = 0
for i in range(len(instructions)):
    instr = instructions[i]
    opcode = instr[0]
    a,b,c = instr[1], instr[2], instr[3]
    bef = before[i]
    expected = after[i]
    # Run all opcodes and check if input behaves appropriately
    working_opcodes = 0 # that works
    f_cnt = 0
    for f in functions:
        # Reset registers to values before op
        r[0], r[1], r[2], r[3] = bef[0], bef[1], bef[2], bef[3]
        # Run all possible operations
        f(a,b,c)
        # Check if result is as expected
        if (r[0] == expected[0] and r[1] == expected[1]
                and r[2] == expected[2] and r[3] == expected[3]):
            working_opcodes += 1
            function[opcode][f_cnt] += 1
        f_cnt += 1
    # If the sample behaves as 3 or more opcodes, add it to samples
    # This is used for part 1
    if working_opcodes >= 3:
        samples += 1

print "%d samples behave like three or more opcodes" % samples

# Find all possible programs for each opcode
viable_progs = []
for opcode in function:
    viable_f = []
    max_value = max(opcode)
    for f in range(len(opcode)):
        if opcode[f] == max_value:
            viable_f += [f]
    viable_progs += [viable_f]
# Find the program of each opcode
programs = {} # give opcode as key
taken = []
count = 0
while not len(programs) == len(function):
    count += 1
    for i in range(len(viable_progs)):
        if len(viable_progs[i]) == 1:
            programs[i] = viable_progs[i][0]
            taken += [viable_progs[i][0]]
            for j in range(len(viable_progs)):
                opcode =  filter(lambda a: a != programs[i], viable_progs[j])
                viable_progs[j] = opcode

# Part 2, execute program
r[0],r[1],r[2],r[3] = 0,0,0,0
for instruction in test_program:
    opcode = instruction[0]
    a,b,c = instruction[1], instruction[2], instruction[3]
    functions[programs[opcode]](a,b,c)
print r[0]









            

