from enum import Enum
from collections import Counter

file = open("./input.txt").readlines()

inputs = [
    (line.split(" ")[0].strip(), int(line.split(" ")[1].strip())) for line in file
]

strength = {
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 8,
    "T": 9,
    "J": 10,
    "Q": 11,
    "K": 12,
    "A": 13,
}


class CardCombination(Enum):
    FIVE_OF_A_KIND = 1
    FOUR_OF_A_KIND = 2
    FULL_HOUSE = 3
    THREE_OF_A_KIND = 4
    TWO_PAIR = 5
    ONE_PAIR = 6
    HIGH_CARD = 7

    def __str__(self) -> str:
        return self.name


class Hand:
    label: int = None
    bid: int = None
    card: str = None
    list_card: list = None

    def __init__(self, card, bid):
        self.card = card
        self.list_card = list(card)
        self.label = self.detect_type()
        self.bid = bid

    def detect_type(self):
        # Create a counter object from the hand list which counts the occurrence of each card in the hand.
        counter = Counter(self.list_card)

        # Get the frequencies of the cards in descending order
        card_fequencies = [count for _, count in counter.most_common()]

        match card_fequencies:
            case [5]:
                return CardCombination.FIVE_OF_A_KIND
            case [4, 1]:
                return CardCombination.FOUR_OF_A_KIND
            case [3, 2]:
                return CardCombination.FULL_HOUSE
            case [3, 1, 1]:
                return CardCombination.THREE_OF_A_KIND
            case [2, 2, 1]:
                return CardCombination.TWO_PAIR
            case [2, 1, 1, 1]:
                return CardCombination.ONE_PAIR
            case _:
                return CardCombination.HIGH_CARD

    def __lt__(self, other: "Hand"):
        if self.label != other.label:
            return self.label.value < other.label.value

        for i in range(5):
            if self.list_card[i] != other.list_card[i]:
                return strength[self.list_card[i]] > strength[other.list_card[i]]

    def __str__(self):
        return f"{self.label} @ C: {self.card} B: {self.bid}"


hands = [Hand(x[0], x[1]) for x in inputs]

# sort hands
hands.sort(reverse=True)

count = 0

for i, hand in enumerate(hands):
    rank = i + 1
    count += hand.bid * rank

print(count)
