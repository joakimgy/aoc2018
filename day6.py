import sys
import datetime
import re

# Set input data file
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "input6.txt"
input_data = open(filename, "r").readlines()
alphabet = "abcdefghijklmnopqrstuvwxyz"

# Parse all coordinates and find grid size
coords = {} # (id, x, y, distance, inf_dist)
max_x = -1
max_y = -1
for i in range(0, len(input_data)):
    x_coord = int(input_data[i].split()[0][:-1])
    y_coord = int(input_data[i].split()[1])
    coords[i+1] = [i+1, x_coord, y_coord, 0, False]
    max_x = x_coord if x_coord > max_x else max_x
    max_y = y_coord if y_coord > max_y else max_y

# Create grid with known coordinates
grid = [[0 for _ in range(max_y+1)] for _ in range(max_x+1)]
for key in coords:
    coord = coords[key]
    grid[coord[1]][coord[2]] = coord[0]

# For task b - positions with total path to all coords < 10,000
area_within_range = 0

# Iterate the grid and find closest known coordinate for each position
for x in range(0, max_x+1):
    for y in range(0, max_y+1):
        min_dist = 10000
        closest_to = -1
        same_dist = 0
        total_range = 0
        # Find minimum manhattan distance of the current pos
        # compared with all known coords 
        for key in coords:
            coord = coords[key]
            if x == coord[1] and y == coord[2]:
                closest_to = coord[0]
            manh_dist = abs(x-coord[1])+abs(y-coord[2])
            total_range += manh_dist
            if manh_dist == min_dist:
                same_dist = 1 # manh_dist same for two coords
            elif manh_dist < min_dist:
                same_dist = 0
                min_dist = manh_dist
                closest_to = coord[0]
        # Extend area_within_range if all coords are closer than 10k
        if total_range < 10000:
            area_within_range +=1
        # Pass if x,y is on a coord
        if closest_to == -1:
            continue
        # Set pos with multiple closest coords to -1
        elif same_dist == 1:
            grid[x][y] = -1
        # Otherwisest set the closest known coord for each pos
        else:
            grid[x][y] = closest_to

# Find largest area
for x in range(0, max_x+1):
    for y in range(0, max_y+1):
        closest = grid[x][y]
        if closest == -1:
            continue # If closest to two do nothing
        elif x == 0 or x == max_x or y == 0 or y == max_y:
            coords[closest][4] = True # inf dist if on border
        else:
            coords[closest][3] += 1 # increment area

# print largest area
largest_area = -1
for key in coords:
    if coords[key][4]:
        continue
    elif coords[key][3] > largest_area:
        largest_area = coords[key][3]

print "The largest area is %d" % largest_area
print "There are %d positions within 10,000" % area_within_range





