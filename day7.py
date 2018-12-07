import sys
import datetime
import re

# Set input data file
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "input7.txt"
input_data = open(filename, "r").readlines()

# Variables
available = []
finished = ""

# Task 2 variables
no_workers = 5
workers = {} # key: id, data: (task, remaining_time)
no_working = 0
in_progress = {} # tasks in progress

# Parse data
prereqs = {} # key: step, data: prereqs
for line in input_data:
    prereq, step = line.split()[1], line.split()[-3]
    if step in prereqs:
        prereqs[step] += [prereq]
    else:
        prereqs[step] = [prereq]

# Add all characters without prereqs to available
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for c in alphabet:
    if c not in prereqs:
        available += [c]

# Find new available steps 
def find_available():
    global prereqs, available, finished, in_progress
    for step in prereqs:
        if step in available or step in finished or step in in_progress:
            continue
        ready = True
        for prereq in prereqs[step]:
            if prereq not in finished:
                ready = False
        if ready:
            available += step

# Task 1
#while True:
#    if available:
#        sorted_available = sorted(available)
#        finished += sorted_available[0]
#        available = sorted_available[1:]
#    else:
#        break
#    find_available()
#print "Task 1 ordering: %s" % finished



# Check if a worker is available, return id
def worker_available(workers):
    for worker in workers:
        if workers[worker][0]=="":
            return worker
    return 0

# Execute tasks for each worker
def execute_work():
    global workers, finished, no_working, in_progress
    for worker in workers:
        if workers[worker][0]:
            workers[worker][1] -= 1
            # If work is done, set task to finished
            if workers[worker][1] == 0:
                del in_progress[workers[worker][0]]
                finished += str(workers[worker][0])
                workers[worker][0] = ""
                no_working -= 1

# Init workers
for i in range(1, no_workers+1):
    workers[i] = ["", 0]

time = 0
while True:
    # Find available workers
    find_available()
    # Dedicate available tasks to available workers
    while available and worker_available(workers):
        worker = worker_available(workers)
        sorted_available = sorted(available)
        task = sorted_available[0]
        available = sorted_available[1:]
        workers[worker] = [task, alphabet.index(task)+62]
        in_progress[task] = 1
        no_working += 1
    # Execute tasks for each worker
    execute_work()
    find_available()
    time += 1
    # If there are no tasks and workers are done, we're done
    if not available and no_working == 0:
        print "It took %d seconds to finish with %d workers." % (time, no_workers)
        print "Ordering is: %s" % finished
        break



























