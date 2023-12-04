cards = open("./input.txt").readlines()
count = 0

for card in cards:
    card = card.split(":")[1].split("|")

    # Parse the winning and have sets
    winning = set([int(x) for x in card[0].strip().split()])
    have = set(int(x) for x in card[1].strip().split())

    # Find the intersection of the two sets
    wins = set(x for x in have if x in winning)

    if len(wins) > 0:
        count += 2 ** (len(wins) - 1)

print(count)
