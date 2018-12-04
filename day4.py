import sys
import datetime
import re

# Set input data file
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "input4.txt"
input_data = open(filename, "r")

# Variables
guard_records = {} # id = [(year, month, day, hour, minute, order)]
current_guard = -1

# Sort all entries after time
data = sorted(input_data.readlines())
# Parse all guard records and add them into a dictionary
for line in data:
    pattern = re.compile("([0-9]+)-([0-9]+)-([0-9]+).([0-9]+):([0-9]+)..([G|w|f])")
    result = pattern.search(line)
    if result:
        year = int(result.group(1))
        month = int(result.group(2))
        day = int(result.group(3))
        hour = int(result.group(4))
        minute = int(result.group(5))
        order = result.group(6) # w=wakes up, f=falls asleep, G=Guard begins
        if (order == "G"):
            current_guard = int(line.split(" ")[-3][1:])
        record = [(year, month, day, hour, minute, order)]
        if current_guard in guard_records:
            guard_records[current_guard] += record
        else:
            guard_records[current_guard] = record

# Find the guard who loves to dream the most
max_sleep = -1
guard_dreaming = -1
for guard in guard_records:
    records = guard_records[guard]
    guard_records[guard] = records
    # Calculate total time slept
    falling_asleep = 0
    waking_up = 0
    for record in records:
        if record[5] == "f":
            falling_asleep += record[4]
        if record[5] == "w":
            waking_up += record[4]
    time_slept = waking_up-falling_asleep
    if time_slept > max_sleep:
        max_sleep = time_slept
        guard_dreaming = guard

print "Guard %s loves sleeping. He slept %d minutes." % (guard_dreaming, max_sleep)

# Find out how much each guard sleeps each minutes
peak_min = -1       # The minute someone slept most at
peak_min_time = -1  # The number of times someone slept at that minute
peak_min_guard = -1 # The guard that slept at that minute
for guard in guard_records:
    sleep_pattern = [0]*60
    sleep_start = 0
    for record in guard_records[guard]:
        if record[5] == "f":
            sleep_start = record[4]
        if record[5] == "w":
            for i in range(sleep_start, record[4]):
                sleep_pattern[i] += 1
    sleep_min = sleep_pattern.index(max(sleep_pattern))
    if max(sleep_pattern) > peak_min_time:
        peak_min = sleep_min
        peak_min_time = max(sleep_pattern)
        peak_min_guard = guard
    if guard == guard_dreaming:
        print "He slept the most at 00:%d" % sleep_min

print "Guard %d slept the most during a specific minute (at 00:%d)" % (peak_min_guard, peak_min)








