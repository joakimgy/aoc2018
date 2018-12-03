import sys

# Set input data file
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "input2.txt"
input_data = open(filename, "r")
data = input_data.readlines()

# Variables
twos = 0
threes = 0

# Go through each box id and check for those id's
# contaning either exactly two or exactly three of one letter
for box_id in data:
    characters = {}
    dup_found2 = False
    dup_found3 = False
    for c in box_id:
        if c in characters:
            characters[c] += 1
        else:
            characters[c] = 1
    for key in characters:
        if characters[key] == 2 and not dup_found2:
            twos += 1
            dup_found2 = True
        if characters[key] == 3 and not dup_found3:
            threes += 1
            dup_found3 = True

print "Checksum is " + str(int(twos)*int(threes))

# Find common characters of IDs which differ exactly one character
for current_box in data:
    for other_box in data:
        pos_difference = -1
        no_diff_chars = 0
        # Compare the characters in the box IDs for one different char
        for i in range (0, len(current_box)-1):
            if current_box[i] is not other_box[i]:
                no_diff_chars += 1
                pos_difference = i
                if no_diff_chars > 1:
                    break;

        # Parse the string excluding the different char
        if no_diff_chars is 1:
            res = ""
            for i in range(0, len(current_box)-1):
                if i is pos_difference:
                    continue
                res += current_box[i] 
            print "The common letters between box IDs are: " + res

