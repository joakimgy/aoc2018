import sys

# Set input data file
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "input14.txt"
input_data = int(open(filename, "r").read())
input_data = "320851"

# Variables
recipes = [3, 7] # all recipes
elves = {0:0, 1:1} # recipe number held by each elf
no_recipes = input_data
pattern = str(input_data)
input_len = len(str(pattern))
score = ""

# Create new recipes based on the sum of the elves recipes
def create_recipes(elves, recipes):
    new_recipe = 0
    for elf in elves:
       new_recipe += recipes[elves[elf]]
    for r in str(new_recipe):
        recipes += [int(r)]

# Each elf picks a new recipe equals to current score + 1
def pick_new_recipe(elves, recipes):
    for elf in elves:
        steps = recipes[elves[elf]]+1
        elves[elf] = (elves[elf]+steps)%len(recipes)

# Make all necessary recipes
# Elves think they have improved affter no_recipes recipes
# Check the next 10 recipes to see if that's true.
def part1():
    global recipes, elves, no_recipes, score
    while len(recipes) < no_recipes+10:
        create_recipes(elves, recipes)
        pick_new_recipe(elves, recipes)
    for i in range(no_recipes, no_recipes+10):
        score += str(recipes[i])
    print "After %d recipes, the next ten has a score of %s." % (no_recipes, score)


prev_len = 2
done = False
while not done:
    # Add recipes and change current recipe for elves
    create_recipes(elves, recipes)
    pick_new_recipe(elves, recipes)
    # Check if pattern is found
    # Handle multiple recipes addeds at once
    recipes_added = len(recipes)-prev_len
    prev_len = len(recipes)
    for i in range(0, recipes_added):
        if i == 0:
            p = "".join(map(str, recipes[-input_len-i:]))
        else:
            p = "".join(map(str, recipes[-input_len-i:-i]))
        if p == pattern:
            print "Done after %d recipes." % (len(recipes)-i-input_len)
            done = True
            break











