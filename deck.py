class Card:
    def __init__(self, color, number):
        self.color = color
        self.number = number

    def __str__(self):
        return "This card is a {color} {number}".format(color=self.color, number=self.number)


class Stack:
    def __init__(self, cards_in_stack):
        self.cards_in_stack = cards_in_stack

    def __str__(self):
        return "There are {num_cards} in this stack.".format(num_cards = len(self.cards_in_stack))

    def check_card_types(self):
        card_tracker = {}
        for card in self.cards_in_stack:
            card_value = "{color} {number}".format(color=card.color, number = card.number)
            if card_value in card_tracker.keys():
                card_tracker[card_value] +=1
            else:
                card_tracker[card_value] = 1


    def add_card_to_stack(self, card):
        self.cards_in_stack.append(card)


class Deck(Stack):
    def shuffle(self):
        pass


class StackInPlay(Stack):
    def check_availability(self):
        pass

    def clear_stack(self):
        pass


class Player:
    pass


class Dice:
    pass