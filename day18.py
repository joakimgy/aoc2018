import sys

# Set input data file
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "input18.txt"
input_data = open(filename, "r").readlines()

# Parse input data
def construct_area(input_data):
    area = [["." for _ in range(len(input_data[0])-1)] for _ in range(len(input_data))]
    for i in range(len(input_data)):
        row = input_data[i]
        for j in range(len(row)-1):
            acre = row[j]
            area[i][j] = acre
    return area

# Return a tuple containing the number of adjacent acres
# Return (open, wooded, lumberyard)
def adjacent_acres(area, row, col):
    # Number of open, wooded, lumberyard acre
    open_acres, wooded_acres, lumberyards = 0, 0, 0
    # Handle edge cases
    from_row = row-1 if row>0 else 0
    to_row = row+1 if row<len(area)-1 else len(area)-1
    from_col = col-1 if col>0 else 0
    to_col = col+1 if col<len(area[0])-1 else len(area[0])-1
    for r in range(from_row, to_row+1):
        for c in range(from_col, to_col+1):
            if row == r and col == c:
                continue
            elif area[r][c] == ".":
                open_acres += 1
            elif area[r][c] == "|":
                wooded_acres += 1
            elif area[r][c] == "#":
                lumberyards += 1
    return (open_acres, wooded_acres, lumberyards)

# Decide what the given acre will look like the next minute
def new_acre(current_acre, adj_open, adj_wood, adj_lumberyards):
    # An open acre will become filled with trees if three or more
    # adjacent acres contained trees
    if current_acre == "." and adj_wood >= 3:
        return "|"
    elif current_acre == "|" and adj_lumberyards >= 3:
        return "#"
    elif current_acre == "#":
        if adj_lumberyards >= 1 and adj_wood >= 1:
            return "#"
        else:
            return "."
    else:
        return current_acre

# Copy an area
def copy_area(area):
    new_area = [["." for _ in range(len(area[0]))] for _ in range(len(area))]
    for row in range(len(area)):
        for col in range(len(area[row])):
            new_area[row][col] = area[row][col]
    return new_area

# Count the number of resources in an area
# Return (open_acres, wooded_acres, lumberyards)
def count_resources(area):
    no_open, no_wood, no_lumberyards = 0,0,0
    for row in area:
        for acre in row:
            if acre == ".":
                no_open += 1
            elif acre == "|":
                no_wood += 1
            elif acre == "#":
                no_lumberyards += 1
    return (no_open, no_wood, no_lumberyards)

# Print the area
def print_area(area):
    for acres in area:
        print "".join(acres)
    print ""

# Construct area with input and let it grow old...
area = construct_area(input_data)
new_area = copy_area(area)
minute = 0
#print "Initial state:"
#print_area(area)
# Variables for part 1 and part 2
r_values = {}
r_10 = ""
# Let the area change for n minutes
n = 1000
while minute < n:
    for row in range(len(area)):
        for col in range(len(area[row])):
            acre = area[row][col]
            adj = adjacent_acres(area, row, col)
            acre = new_acre(acre, adj[0], adj[1], adj[2])
            new_area[row][col] = acre
    area = copy_area(new_area)
    minute += 1
    #print "After %d minutes:" % minute
    #print_area(area)
    r = count_resources(area)
    r_value = r[1]*r[2]
    # Part 1
    if minute == 10:
        r_10 = (r[0], r[1], r[2], r_value)
    # Part 2
    # Let the area settle to a fixed pattern...
    # Save the minutes at which each resource value appears
    if minute >= 500:
        if r_value in r_values:
            r_values[r_value] += [minute]
        else:
            r_values[r_value] = [minute]

# Part 1
print "Part 1:"
print "10 minutes have passed..."
print ("There are %d open acres, %d wooded acres and %d lumberyards." 
    % (r_10[0],r_10[1],r_10[2]))
print "The total resource value is %d" % r_10[3]
print ""

# Part 2
print "Part 2:"
no_patterns = len(r_values) # The number of unique areas after area has settled
# Find pattern for 500th
for r_value in r_values:
    if r_values[r_value][0] % no_patterns == 1000000000 % no_patterns:
        print "The resouce value after 1,000,000,000 minutes will be", r_value








