import sys
import llist

# Set input data file
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "input9.txt"
input_data = open(filename, "r").read().split()

# Parameters
players = int(input_data[0])
last_marble = int(input_data[6])*100

# Variables
turn = 1
marbles = llist.dllist([0])
score = {}
for i in range(0, players):
    score[i] = 0

# Play the game!
current = marbles.first
while turn <= last_marble:
    # Normal turn - not multiple of 23
    if turn % 23:
        if current.next:
            if current.next.next:
                current = marbles.insert(turn, current.next.next)
            else:
                current = marbles.append(turn)
        else:
            current = marbles.insert(turn, marbles.first.next)
    # Special turn - multiple of 23
    else:
        # Go back 7 marbles counter-clockwise
        for i in range(0,6):
            if current.prev:
                current = current.prev
            else:
                current = marbles.last
        # Increase player's score
        if current.prev:
            score[turn%players] += turn + marbles.remove(current.prev)
        else:
            score[turn%players] += turn + marbles.remove(marbles.last)

    turn += 1

# Print score
max_score = 0
for player in score:
    max_score = score[player] if score[player] > max_score else max_score

print "Max score is: %d" % max_score



