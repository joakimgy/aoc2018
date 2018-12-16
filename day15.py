import sys
import collections

# Set input data file
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "input15.txt"
input_data = open(filename, "r").readlines()

# Parameters
reading_order = ["UP", "LEFT", "RIGHT", "DOWN"]

# Create cave given input data
def create_cave(input_data):
    cave = []
    for i in range(len(input_data)):
        row = input_data[i]
        r = []
        r += row
        cave += [r]
    return cave

# Find NPCs, return dict's with goblin/elf information
def find_npcs(cave, elves_atk):
    npcs, g, e, cnt ={}, 0, 0, 1
    for row in range(len(cave)):
        for col in range(len(cave[0])):
            if cave[row][col] == "G":
                npcs[cnt] = [row,col,200, 3, "G"]
                cnt += 1
                g += 1
            elif cave[row][col] == "E":
                npcs[cnt] = [row,col,200, elves_atk, "E"]
                cnt += 1
                e += 1
    return [g, e, npcs]

# Prints the current cave/state
def print_cave(cave):
    for r in cave:
        print "".join(r)

def print_npcs(npcs):
    for n in npcs:
        print n, npcs[n]

# Play a turn in the given cave, return new state
def play_turn(cave): 
    return 0

# Find the position of enemy target closest to unit
# Returns [position, next_square, distance]
def find_target(cave, npcs, npc_id):
    npc = npcs[npc_id]
    target_type = "E" if npc[4] == "G" else "G" # Elf or goblin target
    dist = 0 # Distance to target
    new_squares = [[npc[0], npc[1], []]] # [[row, col, path], ..]
    targets, reachable = [], []
    # Find a target recursively
    while not targets:
        if not new_squares: # Target not found
            return [[], -1]
        ns = []
        # Find squares adjacent of current square
        for sq in new_squares:
            path = sq[2] + [[sq[0], sq[1]]]
            n,w = [sq[0]-1, sq[1]], [sq[0], sq[1]-1]
            e,s = [sq[0], sq[1]+1], [sq[0]+1, sq[1]]
            sqs = [n,w,e,s]
            # Check adjacent squares
            for s in sqs:
                if s in reachable:
                    continue # only check squares once
                s_type = cave[s[0]][s[1]]
                if s_type == target_type:
                    targets += [[s, path]] # If target is found, add it to targets
                if s_type == ".":
                    ns += [[s[0], s[1], path]] # If the square type is walkable, check it
                    reachable += [s]
        new_squares = ns
        dist += 1
    target = min(targets) # pos, path, distance
    return [target[0], target[1], dist]

# Return npc id of a position (npc must be alive)
def npc_at(npcs, row, col):
    for npc_id in npcs:
        npc = npcs[npc_id]
        if npc[0] == row and npc[1] == col and npc[2] > 0:
            return npc_id
    return False

# Walk toward a position
def walk_to(cave, npcs, npc_id, path):
    # Remove npc from map
    npc = npcs[npc_id]
    cave[npc[0]][npc[1]] = "."
    # Move npc, and add to map
    npc[0], npc[1] = path[0], path[1]
    cave[npc[0]][npc[1]] = npc[4]


# Attack adjacent target
def attack_target(cave, npcs, npc_id):
    global goblins, elves
    npc = npcs[npc_id]
    target_type = "E" if npc[4] == "G" else "G" # Elf or goblin target
    targets = []
    target_id = 0
    # Find target with lowest hp
    if cave[npc[0]-1][npc[1]] == target_type: # north
        targets += [[npc[0]-1, npc[1]]]
    if cave[npc[0]][npc[1]-1] == target_type: # west
        targets += [[npc[0], npc[1]-1]]
    if cave[npc[0]][npc[1]+1] == target_type: # east
        targets += [[npc[0], npc[1]+1]]
    if cave[npc[0]+1][npc[1]] == target_type: # south
        targets += [[npc[0]+1, npc[1]]]
    if targets:
        lowest_hp = 1000
        for t in targets:
            t_id = npc_at(npcs, t[0], t[1])
            if npcs[t_id][2] < lowest_hp and npcs[t_id][2] > 0:
                lowest_hp = npcs[t_id][2]
                target_id = t_id
    if not target_id:
        return -1
    # Do damage to target
    npcs[target_id][2] -= npcs[npc_id][3]
    # If target dies, remove it from map
    if npcs[target_id][2] <= 0:
        cave[npcs[target_id][0]][npcs[target_id][1]] = "."
        if npcs[target_id][4] == "G":
            goblins -= 1
        else:
            elves -= 1
        
        

# Order npcs according to reading order
def reorder(npcs):
    return (collections.OrderedDict(sorted(npcs.iteritems(),
        key=lambda(k,v):(v,k))))

# Initiate the program
counter = 0
while True:
    cave = create_cave(input_data)
    n = find_npcs(cave, 3+counter) # Start with 3ATK for elves, then +1/round
    goblins, elves, npcs = n[0], n[1], n[2]
    init_elves = elves # For part 2

    # Run the program
    turn = -1
    while goblins>0 and elves>0:
        npcs = reorder(npcs)
        # Play turn for each nps
        for npc_id in npcs:
            if npcs[npc_id][2] <= 0:
                continue # NPC is dead, do nothing
            target = find_target(cave, npcs, npc_id)
            if target[-1] == -1: # Nothing to do, stay idle
                continue
            if target[2] > 1: # If not adjacent to target, walk there
                path = target[1][1]
                walk_to(cave, npcs, npc_id, path)
            target = find_target(cave, npcs, npc_id)
            if target[2] == 1:
                attack_target(cave,npcs,npc_id)
        # Increment turn
        turn += 1

    # Task 1
    # Print turn and remaining hp when someone wins
    if counter == 0:
        # Find sum of all remaining survivors:
        sum_hp = 0
        for npc in npcs.values():
            if npc[2] > 0:
                sum_hp += npc[2]
        print "Task 1:"
        print "Remaining hp after %d turns is %d" % (turn, sum_hp)
    # If all elves survive, stop and print atk
    if elves == init_elves:
        print ""
        print "Task 2:"
        print "All elves survived with attack power %d" % (3+counter)
        sum_hp = 0
        for npc in npcs.values():
            if npc[2] > 0:
                sum_hp += npc[2]
        print "Remaining hp after %d turns is %d" % (turn, sum_hp)
        break
    counter += 1










