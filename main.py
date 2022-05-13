print("Hello World")
import deck


colors = ['Red', 'Blue', 'Yellow','Green', 'Purple']
numbers = [str(x) for x in range(1,7)]
copies_of_number = 3

numbered_cards = []
for color in colors:
    for number in numbers:
        for i in range(copies_of_number):
            card = Card(color, number)
            numbered_cards.append(card)

assert len(numbered_cards) == 90

deck = Deck(numbered_cards)
print(deck)