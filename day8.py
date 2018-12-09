import sys

# Set input data file
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "input8.txt"
input_data = open(filename, "r").read().split()

# Variables
pointer = 0
all_meta_data = []
    
# Add the node which pointer is pointing on
# If pointer is on root, construct the entire tree
def add_node():
    global input_data, pointer, all_meta_data
    header = input_data[pointer:pointer+2]
    no_child = int(header[0])
    no_meta = int(header[1])
    node = [no_child, no_meta, [], []]
    pointer += 2
    # Add new nodes (children)
    for i in range(0, no_child):
        node[3] += [add_node()]
    # Add meta data
    for i in range(0, no_meta):
        node[2] += [int(input_data[pointer])]
        all_meta_data += [int(input_data[pointer])]
        pointer += 1

    return node

# Build tree
tree = add_node() # [no_child, no_meta, [metadata], [children]]

res = map(int, all_meta_data)
print "The sum of the metadata is %d" % sum(res)


# Find the value of a node (task 2)
def find_value(node):
    value = 0
    # If no children, return sum of metadata
    if not node[3]:
        return sum(node[2])
    # Value = sum of all children specified by indexes
    for index in node[2]:
        if index > len(node[3]):
            continue # If invalid reference, skip it
        if index == 0:
            continue
        value += find_value(node[3][index-1])
    return value

print "The value of the root node is %d" % find_value(tree)
