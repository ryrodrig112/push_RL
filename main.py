print("Hello World")


class Card:
    def __init__(self, color, number):
        self.color = color
        self.number = number

    def __str__(self):
        return "This card is a {color} {number}".format(color = self.color, number = self.number)


class Stack:
    pass


class Player:
    pass


class Dice:
    pass


card = Card("Red", "6")
print(card)