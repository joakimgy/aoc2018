import sys
import collections

# Set input data file
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "input13.txt"
input_data = open(filename, "r").readlines()

# Variables
track = [] # Contains track
track_state = [] # Contains track + carts
carts = {} # Info on all the carts [y,x,direction, intersection, collided]
           # insersection: [0=left, 1=straight, 2=right]
no_carts = 0

# Parse input, create track grid
cart_id = 1
for y in range(0, len(input_data)):
    line = []
    line += input_data[y]
    track_state += [line]
    track_part = []
    track_part += line
    for x in range(0, len(line)):
        c = line[x]
        if c == ">" or c == "<":
            track_part[x] = "-"
            carts[cart_id] = [y,x,c,0, False]
            cart_id += 1
        elif c == "^" or c == "v":
            track_part[x] = "|"
            carts["%s" % cart_id] = [y,x,c,0, False]
            cart_id += 1
    track += [track_part]
no_carts = len(carts)

# Check if there is a cart at x,y
def iscart(x,y):
    global track_state
    t = track_state[y][x]
    if t == "<" or t == ">" or t == "^" or t == "v":
        return True
    return False

# Return id of cart at x,y
def find_cart(x,y):
    global carts
    for cart in carts:
        c = carts[cart]
        if c[1]==x and c[0]==y and not c[4]:
            return cart

# Move cart with cart_id one step
# Return False if collision
def movecart(cart_id):
    global carts, track_state, track_state, no_carts
    cart = carts[cart_id]
    # Find new position
    new_x, new_y = cart[1], cart[0]
    if cart[2] == "<":
        new_x -= 1
    elif cart[2] == ">":
        new_x += 1
    elif cart[2] == "^":
        new_y -= 1
    elif cart[2] == "v":
        new_y += 1
    # Remove cart from old position
    track_state[cart[0]][cart[1]] = track[cart[0]][cart[1]]
    # Handle intersections and turns
    loc = track[new_y][new_x]
    cd = cart[2]
    if loc == "+": # intersection
        if cart[3] == 0: # turn left
            nd = {"<":"v", ">":"^", "^":"<", "v":">"} 
            carts[cart_id][2] = nd[cd]
        if cart[3] == 2: # turn right
            nd = {"<":"^", ">":"v", "^":">", "v":"<"}
            carts[cart_id][2] = nd[cd]
        carts[cart_id][3] = (carts[cart_id][3]+1)%3
    elif loc == "\\":
        nd = {"<":"^", ">":"v", "^":"<", "v":">"}
        carts[cart_id][2] = nd[cd]
        pass
    elif loc == "/":
        nd = {"<":"v", ">":"^", "^":">", "v":"<"}
        carts[cart_id][2] = nd[cd]
    # Check for collision, otherwise move cart
    if iscart(new_x, new_y):
        carts[cart_id][4] = True # collided is true for current cart
        carts[find_cart(new_x,new_y)][4] = True # collided true other cart
        track_state[new_y][new_x] = track[new_y][new_x] # remove other cart
        if no_carts == len(carts):
            print "First collision at (%d, %d)" % (new_x, new_y)
        no_carts -= 2
        return False
    else:
        track_state[new_y][new_x] = carts[cart_id][2]
        # Add cart to new position
        carts[cart_id][1] = new_x
        carts[cart_id][0] = new_y
        return True

# Reorder cart order based on y then x position
def reorder_carts():
    global carts
    carts = collections.OrderedDict(sorted(carts.iteritems(), key=lambda (k,v):(v,k)))

# Run the cart system until first collision
tick = 0
while no_carts > 1:
    tick += 1
    reorder_carts()
    for cart in carts:
        if carts[cart][4]:
            continue # if cart has collided, dont do anything
        else:
            movecart(cart)

# Find position of last cart
for cart in carts:
    c = carts[cart]
    if not c[4]:
        print "Last cart is at pos (%d, %d)" % (c[1], c[0])










