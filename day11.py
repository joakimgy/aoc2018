import sys

# Set input data file
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "input11.txt"
input_data = open(filename, "r").readline()

# Parse input
#serial_number = int(input_data)
serial_number = 5093

# Create grid
grid = [[0 for _ in range(0,300)] for _ in range(0,300)]
for y in range(0,300):
    for x in range(0,300):
        rack_id = (x+1)+10
        power = rack_id*(y+1)
        power += serial_number
        power *= rack_id
        power = power / 100 % 10
        power -= 5
        grid[y][x] = power

# Find largest size x size fuel cell
def find_cell(size):
    largest_cell = 0
    cell_coord = [0,0]
    for y in range(0,300):
        for x in range(0,300):
            cell_power = 0
            max_size = min(300-x, 300-y)
            for i in range(0,grid_size):
                for j in range(0,grid_size):
                    if y+i<300 and x+j<300:
                        cell_power += grid[y+i-1][x+j-1]
                    else:
                        cell_power = -100
            if cell_power > largest_cell:
                largest_cell = cell_power
                cell_coord = [x,y]
    print "Largest cell with power %d at (%s, %s)" % (largest_cell, cell_coord[0],cell_coord[1])
    print "With cell size: %d" % grid_size

# Try different fuel cell sizes and return highest value
# Stop if fuel is 0 because it won't improve
size = 0
max_cell = 0
for grid_size in range(0,30):
    fuel = find_cell(grid_size)
    if fuel > max_cell:
        max_cell = fuel
        size = grid_size
    if fuel == 0:
        break

print "Found the largest fuel cell, check output"
