import components
import game
import strategies

# params
colors = ['Red', 'Blue', 'Yellow', 'Green', 'Purple']
numbers = [x for x in range(1, 7)]
copies_of_number = 3
num_bombs = 18
num_reverse = 12
num_players = 4

# create dice
dice_sides = colors + [None]
dice = components.Dice(dice_sides)

# instantiate cards
#
numbered_cards = []
bomb_list = []
reverse_list = []
for color in colors:
    for number in numbers:
        for i in range(copies_of_number):
            card = components.Card(color, number)
            numbered_cards.append(card)
for bomb in range(num_bombs):
    card = components.Card("Bomb", "Bomb")
    bomb_list.append(card)
for reverse in range(num_reverse):
    card = components.Card("Reverse", "Reverse")
    reverse_list.append(card)

# instantiate deck
deck = components.Deck(numbered_cards + bomb_list + reverse_list)
deck.shuffle()

# instantiate 3 piles
pile_1 = components.Pile([])
pile_2 = components.Pile([])
pile_3 = components.Pile([])

# instantiate players
names = ["Raphael", "Donatello", "Michelangelo", "Leonardo"]
player_list = []
for name in names:
    player = game.Player(name)
    player_list.append(player)

Push = game.PushGame(player_list, deck, dice)
Push.play()






