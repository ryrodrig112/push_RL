import random


class Card:
    def __init__(self, color, number):
        self.color = color
        self.number = number
        self.active = False

    def __str__(self):
        return "{color} {number}".format(color=self.color, number=self.number)

    def play_card(self):
        pass


class Stack:
    def __init__(self, card_stack):
        self.card_stack = card_stack

    def show(self):
        for card in self.card_stack:
            print(card)

    def count_cards(self):
        return len(self.card_stack)

    def check_card_types(self):
        card_tracker = {}
        for card in self.card_stack:
            card_value = "{color} {number}".format(color=card.color, number=card.number)
            if card_value in card_tracker.keys():
                card_tracker[card_value] += 1
            else:
                card_tracker[card_value] = 1
        return card_tracker

    def add_card_to_stack(self, card):
        self.card_stack.append(card)


class Deck(Stack):
    def shuffle(self):
        random.shuffle(self.card_stack)

    def draw(self):
        card = self.card_stack.pop()
        card.in_play = True
        return card


class Pile(Stack):
    def __init__(self, card_stack):
        self.available = True
        self.card_stack = card_stack

    def check_availability(self, active_card):
        self.available = True
        if self.card_stack:  # Check the cards if there are cards to be checked
            for played_card in self.card_stack:
                if active_card.color == played_card.color:
                    self.available = False
                elif active_card.number == played_card.number:
                    self.available = False
        return self.available

    def show_availability(self, active_card):
        if self.available == True:
            print(f"{active_card} can be played in this pile.".format(active_card))
        else:
            print(f"{active_card} cannot be played in this pile.".format(active_card))

    def clear_stack(self):
        self.card_stack = []


class Dice:
    def __init__(self, sides):
        self.sides = sides

    def roll(self):
        side = random.choice(self.sides)
        return side
