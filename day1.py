import sys

# Set input data file
if len(sys.argv) > 1:
    filename = sys.argv[1];
else:
    filename = "input1.txt"
input_data = open(filename, "r")
data = input_data.readlines()

# Variable
sum = 0;
freq_list = {}
done = False;

# Calculate sum of data
for word in data:
    sum += int(word)
    if str(sum) in freq_list:
        print "The first frequency reached twice is " + str(sum)
        done = True
        break;
    freq_list[str(sum)] = True

print "The resulting frequency is: " + str(sum)

# Look for first frequency that appears twice
while not done:
    for word in data:
        sum += int(word)
        if str(sum) in freq_list:
            print "The first frequency reached twice is " + str(sum)
            done = True
            break;
        freq_list[str(sum)] = True

