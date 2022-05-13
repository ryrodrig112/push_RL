print("Hello World")


class Card:
    def __init__(self, color, number):
        self.color = color
        self.number = number

    def __str__(self):
        return "This card is a {color} {number}".format(color=self.color, number=self.number)


class Stack:
    def __init__(self, cards_in_stack):
        self.cards_in_stack = cards_in_stack


class Player:
    pass


class Dice:
    pass


colors = ['Red', 'Blue', 'Yellow','Green', 'Purple']
numbers = [str(x) for x in range(1,7)]
copies_of_number = 3

all_cards = []
for color in colors:
    for number in numbers:
        for i in range(copies_of_number):
            card = Card(color, number)
            all_cards.append(card)

for card in all_cards:
    print(card)
assert len(all_cards) == 90
