import sys
import time

# Set input data file
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "input19.txt"
input_data = open(filename, "r").readlines()

##############
# Registers
r = {}
pc = 0
pc_r = 0
##############

# Parse first section of input
program = []
for instruction in input_data:
    i = instruction.split()
    if "ip" in instruction:
        pc_r = int(i[1])
    else:
        program += [[i[0], int(i[1]), int(i[2]), int(i[3])]]

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
### PART 1
##################
def part1():
    global pc
    functions = ([addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, 
                gtir, gtri, gtrr, eqir, eqri, eqrr])
    r[0],r[1],r[2],r[3],r[4],r[5] = 0,0,0,0,0,0

    while True:
        # Fetch program counter from register
        if pc >= len(program) or pc < 0:
            break
        r[pc_r] = pc
        # Execute instruction
        ins = program[r[pc_r]]
        globals()[ins[0]](ins[1], ins[2], ins[3])
        # Write new value of pc from register and increment
        pc = r[pc_r] + 1
        
    print "Part 1"
    print "Resulting value in r0 is", r[0]

##################################
### PART 2
##################################

# The program looks like this:
# The first parts set register values
# -> r = [0,0,0,10550400,0,10551276]
# Then there's a nest loop
# while r1 <= r5:
#   r2 = 1
#   r3 = r1*r2
#   if r3 == r5:
#       r0 += r1
#   while r2 <= r5:
#       r2+=1
#   r1 += 1

# If look look specifically at r0 (the if)
# we find that we basically add all terms
# which r5 is dividable with (r5 % term == 0)
def part2():
    r5 = 10551276
    r0 = 0
    for i in range(1,r5+1):
        if (r5%i) == 0:
            r0 += i
    print "Part 2"
    print "Resulting value in r0 is", r0

part1()
part2()
        
        





####################################
### COMMENTS PART 2
####################################
# Program in pseudo code (still low level):
#0  pc = pc+16
#1  r1 = 1
#2  r2 = 1
#3  r3 = r1*r2
#4  if r3 == r5:
#       r3 == 1
#   else:
#    r3 = 0
#5  pc = r3+4
#6  pc = pc+1
#7  r0 = r0+r1
#8  r2 = r2+1
## Loop 1
#9  if r2 > r5:
#       r3 = 1
#   else:
#       r3 = 0
#10 pc = pc+r3
#11 pc = 2
#12 r1 = r1+1
## Loop 2
#13 if r1 > r5:
#       r3 = 1
#   else:
#       r3 = 0
#14 pc = r3+pc
#15 pc = 1
#16 pc = pc^2
#17 r5 = r5+2
#18 r5 = r5^2
#19 r5 = pc*r5
#20 r5 = r5*11
#21 r3 = r3+1
#22 r3 = r3*pc
#23 r3 = r3+18
#24 r5 = r5+r3
#25 pc = pc+r0
#26 pc = 0
#27 r3 = pc
#28 r3 = r3*r4
#29 r3 = pc+r3
#30 r3 = pc*r3
#31 r3 = r3*14
#32 r3 = pc*r3
#33 r5 = r5+r3
#34 r0 = 0
#35 r3 = r3*14
#36 r3 = pc*r3
#37 r5 = r5+r3
#38 r0 = 0
#39 pc = 0















