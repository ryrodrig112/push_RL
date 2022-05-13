import push

print("Hello World")
print('')

colors = ['Red', 'Blue', 'Yellow','Green', 'Purple']
numbers = [str(x) for x in range(1,7)]
copies_of_number = 3

numbered_cards = []
for color in colors:
    for number in numbers:
        for i in range(copies_of_number):
            card = push.Card(color, number)
            numbered_cards.append(card)

assert len(numbered_cards) == 90

active_card = push.Card("Green", '1')
pile_1 = push.Pile([push.Card("Red", "1"), push.Card("Blue", "2")])
pile_1.show()

pile_1.check_availability(active_card)
pile_1.show_availability(active_card)
