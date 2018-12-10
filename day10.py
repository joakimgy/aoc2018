from __future__ import print_function
import sys
import time
from termcolor import colored

# Set input data file
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "input10.txt"
input_data = open(filename, "r").readlines()

# Variables
light_points = {} # [x_pos, y_pos, x_vel, y_vel]

# Find initial positions and velocity
light_id = 0
for line in input_data:    
    x_pos = int(line.split("<")[1].split()[0][:-1])
    y_pos = int(line.split(",")[1].split()[0][:-1])
    x_vel = int(line.split("<")[-1][:2])
    y_vel = int(line.split()[-1][:-1])
    # Add position and velocity data to light point dict
    light_points[light_id] = [x_pos, y_pos, x_vel, y_vel]
    light_id += 1


# Parse light points into position grid
def print_msg(min_x, max_x, min_y, max_y):
    global light_points
    grid = [[0 for _ in range(min_x,max_x+1)] for _ in range(min_y,max_y+1)]
    for point in light_points.values():
        x_pos = point[0]
        y_pos = point[1]
        grid[(max_y-y_pos)][max_x-x_pos] = 8
    for i in range(len(grid)-1, -1, -1):
        for j in range(len(grid[i])-1, -1, -1):
            if grid[i][j] == 0:
                print(colored(grid[i][j], 'grey'), end='')
            else:
                print(colored(grid[i][j], 'red'), end='')
            sys.stdout.flush()
        print("")
    print("")

# Tick 1s - move all lights according to velocity
def tick():
    global light_points
    for key in light_points:
        point = light_points[key]
        point[0] += point[2]
        point[1] += point[3]

step = 0
while step < 10932:
    step += 1
    tick()
    if step == 10932:
        print_msg(106, 167, 136, 145)

# Calculate minimum area of lights
# Step: 10932
# Minimum area: 549
# at position: [106, 167, 136, 145]
def min_area():
    global light_points
    step= 0
    min_area = 10000000000
    min_pos = [0,0,0,0] # min_x, max_x, min_y, max_y
    min_step = 0
    while step < 30000:
        min_x, max_x, min_y, max_y = 1000,-1000,1000,-1000
        for point in light_points.values():
            min_x = min_x if min_x < point[0] else point[0]
            max_x = max_x if max_x > point[0] else point[0]
            min_y = min_y if min_y < point[1] else point[1]
            max_y = max_y if max_y > point[1] else point[1]
        area = (max_x-min_x)*(max_y-min_y)
        if area < min_area:
            min_area = area
            min_pos = [min_x, max_x, min_y, max_y]
            min_step = step
        tick()
        step += 1
    print("Step: %d" % min_step)
    print("Minimum area is: %d" % min_area)
    print("When positions span %s" % min_pos)






