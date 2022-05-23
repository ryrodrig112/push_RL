import random
import components


class Player:
    """Class for one player in the Push game"""

    def __init__(self, name):
        """
        Players are initialized with the following:
            - Name (str): Name of the player
            - Score (int): Initial score of the player - always 0
            - Drawing (bool): Indicates whether the player is going to continue to draw or not
        """
        self.name = name
        self.drawing = True
        self.score = 0

    # Begin turn taking methods - likely will end up as sub-functions within a method
    def choose_pile(self, active_card, available_piles):
        """ Given an active card and set of piles to play to, randomly place the card in a pile"""
        if available_piles:
            selection = random.choice(available_piles)
            return selection
        else:
            return 'Push'  # This needs to be implemented

    def draw_or_pass(self):
        """ Randomly decide whether or not to continue drawing or to pass"""
        self.drawing = random.choice([True, False])

    def reset(self):
        """ Ensure that the player will begin their next turn by drawing"""
        self.drawing = True

    def __str__(self):
        return "{name}: {score} points".format(name=self.name, score=self.score)


class PushGame:
    """Class for the Push Game"""

    def __init__(self, players, deck):
        """
        PushGames are initialized with the following
        :param
            players (list): Players involved in game in turn order)
            deck (list): Stack of cards representing the deck
            piles (list of lists): Piles the active card is played into
            active_card (card): The card most recently drawn off the deck
            available_piles (list): indices of the piles the active card can be played into

            running (bool): Indicator identifying whether game is currently in motion

            winners (list): Winner(s) of the game
            top_score (int): Winning score


        """
        self.players = players
        self.deck = deck
        self.running = False
        self.piles = [components.Pile(None), components.Pile(None), components.Pile(None)]
        self.active_card = None
        self.available_piles = []

        self.winners = None
        self.top_score = None

    def identify_playable_piles(self):
        self.available_piles = []
        for pile_index in range(len(self.piles)):
            if self.piles[pile_index].check_availability(self.active_card):
                self.available_piles.append(pile_index)

    def win(self):
        """Return the player(s) with the highest score in the game"""
        score_dictionary = {player.name: player.score for player in self.players}
        top_score = max(score_dictionary.values())
        winners = [player for player, score in score_dictionary.items() if score == top_score]
        self.winners = winners

    def reset(self, player):
        player.reset()
        self.piles = self.piles = [components.Pile([]), components.Pile([]), components.Pile([])]
        self.available_piles = [0, 1, 2]

    def play(self):
        """Play the game"""
        self.running = True
        while self.running:  # While in running state...
            for player in self.players:  # ...players each take their turn...
                if self.running:
                    self.reset(player)  # ... beginning by drawing at least one card onto the empty piles.
                    while player.drawing: # On their turn a player will draw cards
                        if self.deck.count_cards() > 0:  # assuming there are cards left
                            self.active_card = self.deck.draw()
                            self.identify_playable_piles()
                            selection = player.choose_pile(self.active_card, self.available_piles) # select a
                            # location for the drawn card
                            if selection == "Push":
                                pass
                            else:
                                self.piles[selection].add_card_to_stack(self.active_card)  # and then place it
                            player.draw_or_pass()  # ... until the player decides not to draw anymore and ends their
                            # turn.
                            print(player.name, self.active_card, self.available_piles, selection)
                        elif self.deck.count_cards() == 0:  # The game ends once the deck is empty
                            self.running = False
                            player.drawing = False
                            print('The game is over, there are no more cards')
                            print('')
        # Once the deck is out of cards, determine a winner
        self.win()
        if len(self.winners) == 1:  # If there is a single winner
            print("{winner} wins the game with a score of {score}".format(winner=self.winners[0], score=self.top_score))
        else:  # print the multiple winners
            print("{winners} tied for first with a score of {score}".format(winners=" and ".join(self.winners),
                                                                            score=self.top_score))


