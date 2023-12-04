cards = open("./input.txt").readlines()

count = 0
multiplier = [1 for i in cards]

for i, card in enumerate(cards):
    card = card.split(":")[1].split("|")

    # Parse the winning and have sets
    winning = set([int(x) for x in card[0].strip().split()])
    have = set(int(x) for x in card[1].strip().split())

    # Find the intersection of the two sets
    wins = set(x for x in have if x in winning)

    # Get the multiplier for this card
    cmultiplier = multiplier[i]

    # Set the multiplier for the next cards
    for j in range(i + 1, min(i + len(wins) + 1, len(cards))):
        multiplier[j] += cmultiplier

    count += cmultiplier

print(count)
