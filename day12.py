import sys

# Set input data file
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "input12.txt"
input_data = open(filename, "r").readlines()

# Parameters
initial_state = ""
state = ""
rules = {}
start = 0
no_generations = 200

# Find initial state and rules
counter = 1
for line in input_data:
    if "initial state" in line:
        initial_state = line.split()[-1]
    elif line != '\n':
        rules[counter] = line[:-1]
        counter += 1
state = initial_state

# Append states if necessary
# (including initial_state)
def append_states(state):
    global initial_state, start
    new_state = state
    for i in range(0,3):
        f = {0:3,1:2, 2:1}
        if state[i] == "#":
            new_state = f[i]*'.' + new_state
            initial_state = f[i]*'.' + initial_state
            start += f[i]
        if state[-i-1] == "#":
            new_state = new_state + f[i]*'.' 
            initial_state = initial_state + f[i]*'.'
    return new_state
            

# Find state after one generation
def next_gen():
    global initial_state, rules, state
    state = append_states(state)
    new_state = state
    for i in range(0, len(state)):
        plants = state[i-2:i+3]
        changed_state = False
        for rule in rules.values():
            if plants == rule.split()[0]:
                new_state = new_state[:i] + rule.split()[-1] + new_state[i+1:]
                changed_state = True
        if not changed_state:
            new_state = new_state[:i] + '.' + new_state[i+1:]
    state = new_state
    return state

# Calculate result after 20 gens
sums = [0 for _ in range(0,no_generations)] 
for gen in range(0,no_generations):
    next_gen()
    sum_plants = 0
    for i in range(0,len(state)):
        if state[i] == "#":
            sum_plants += i-start
    sums[gen] = sum_plants
    #print "Sum of plant gen %s is: %d" % (gen+1, sum_plants)
    #print ""

# Task 2
# Difference of sum between generations eventually becomes constant
diffs = sums
task2_gen = 50000000000
for i in range(no_generations-2, 0, -1):
    val = sums[i]
    diffs[i] = sums[i]-sums[i-1]
    if diffs[i] == diffs[i+1]:
        print "Sum of gen %d is %d" % (i+1, val)
        print "Diff of gen %d is %d" % (i+1, diffs[i+1])
        res = val + diffs[i+1]*(task2_gen-i-1)
        print "Sum after %d gens is %d" % (task2_gen, res)
        break






