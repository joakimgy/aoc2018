import sys
import time

# Set input data file
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "input3.txt"
input_data = open(filename, "r")
data = input_data.readlines()

# Variables
fabric_claims = {} # fabric_claims[id] = [x_coord, y_coord, width, height]
max_w = 0
max_h = 0

# Collect data and find max width/height
for line in data:
    claims = line.split(" ")
    claim_id = int(claims[0][1:5])
    xy_coords = map(int, claims[2][:-1].split(",")) # xy_coords = [x,y]
    wh = map(int, claims[3].split("x")) # wh = [widht, height]
    fabric_claims[claim_id] = [xy_coords[0], xy_coords[1], wh[0], wh[1]]
    max_w = xy_coords[0]+wh[0] if xy_coords[0]+wh[0] > max_w else max_w
    max_h = xy_coords[1]+wh[0] if xy_coords[1]+wh[1] > max_h else max_h

# Calculate how many times each square inch
# of the fabric is used
fabric_grid = [[0 for x in range(max_w)] for y in range(max_h)] 
for key in fabric_claims:
    claim = fabric_claims[key]
    # Then loop from y_coord to y_coord+heigth
    # Loop from x_coord to x_coord+width
    for y in range(claim[0], claim[0]+claim[2]):
        for x in range(claim[1], claim[1]+claim[3]):
            # print "[0][0] = %d with coord [%d, %d]" % (fabric_map[0][0], x, y)
            fabric_grid[x][y] = fabric_grid[x][y] + 1


# Find the number of overlapping square inches
overlap_count = 0
for i in range(max_h):
    for j in range(max_w):
        if fabric_grid[i][j] > 1:
            overlap_count += 1

print "Overlap count: " + str(overlap_count)

# Find the non-overlapping fabric
for key in fabric_claims:
    claim = fabric_claims[key]
    intact = True
    for y in range(claim[0], claim[0]+claim[2]):
        if not intact:
            break
        for x in range(claim[1], claim[1]+claim[3]):
            if fabric_grid[x][y] is not 1:
                intact = False
                break;
    if intact:
        print "Non-overlapping ID is #%d" % key
