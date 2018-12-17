import sys

# Set input data file
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "input17.txt"
input_data = open(filename, "r").readlines()

# Find clay and sand positions in map
x_pos = []
y_pos = []
for line in input_data:
    if "x" in line.split(",")[0]:
        x = int(line.split(",")[0][2:])
        x_pos += [[x]]
    elif "x" in line.split(",")[1]:
        x = line.split(",")[1]
        x_start = int(x.split(".")[0][3:])
        x_end = int((x.split(".")[-1]))
        x_pos += [[x_start, x_end]]
    if "y" in line.split(",")[0]:
        y = int(line.split(",")[0][2:])
        y_pos += [[y]]
    elif "y" in line.split(",")[1]:
        y = line.split(",")[1]
        y_start = int(y.split(".")[0][3:])
        y_end = int(y.split(".")[-1])
        y_pos += [[y_start, y_end]]

# Find min and max coordinates and create grid
min_y, max_y, min_x, max_x = 1000, 0, 1000, 0
for i in range(len(y_pos)):
    if len(y_pos[i]) == 2:
        max_y = max(y_pos[i]) if max(y_pos[i]) > max_y else max_y
        min_y = min(y_pos[i]) if min(y_pos[i]) < min_y else min_y
        max_x = max(x_pos[i]) if max(x_pos[i]) > max_x else max_x
        min_x = min(x_pos[i]) if min(x_pos[i]) < min_x else min_x
    else:
        max_y = y_pos[i][0] if y_pos[i][0] > max_y else max_y
        min_y = y_pos[i][0] if y_pos[i][0] < min_y else min_y
        max_x = x_pos[i][0] if x_pos[i][0] > max_x else max_x
        min_x = x_pos[i][0] if x_pos[i][0] < min_x else min_x

grid = [["." for _ in range(min_x,max_x+1)] for _ in range(min_y,max_y+1)]

# Scan ground (grid) and fill with sand wherever found
for i in range(len(x_pos)):
    if len(x_pos[i]) == 1:
        for y in range(y_pos[i][0], y_pos[i][1]+1):
            grid[y-min_y][x_pos[i][0]-min_x] = "#"
    elif len(y_pos[i]) == 1:
        for x in range(x_pos[i][0], x_pos[i][1]+1):
            grid[y_pos[i][0]-min_y][x-min_x] = "#"
grid[0][500-min_x] = "+"
for g in grid:
    print g

# Add water
tick = 0
while tick < 2:
    tick += 1



















