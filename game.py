import random
import components


class Player():
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
    @staticmethod
    def choose_pile(active_card, available_piles):
        """ Given an active card and set of piles to play to, randomly place the card in a pile"""
        if available_piles:
            selection = random.choice(available_piles)
            PushGame.piles[selection].add_card_to_stack(active_card)
            print(selection)
        else:
            print('Push')  # Come back to this

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
            check = self.piles[pile_index].check_availability(self.active_card)
            if check:
                self.available_piles.append(check)

    def win(self):
        """Return the player(s) with the highest score in the game"""
        score_dictionary = {player.name: player.score for player in self.players}
        top_score = max(score_dictionary.values())
        winners = [player for player, score in score_dictionary.items() if score == top_score]
        self.winners = winners

    def play(self):
        """Play the game"""
        self.running = True
        while self.running:
            for player in self.players:  # For each player in the game...
                if self.running:
                    player.reset()  # Make sure that player will draw at least one card this turn
                    print(player, self.deck.count_cards(), player.drawing, self.running)
                    while player.drawing:  # ... draw and place cards until you decide to stop...
                        if self.deck.count_cards() > 0:  # While there are cards remaining in the deck, players take
                            # turns
                            self.active_card = self.deck.draw()
                            self.identify_playable_piles()
                            player.choose_pile(self.active_card, self.available_piles)
                            player.draw_or_pass()
                        elif self.deck.count_cards() == 0:
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


