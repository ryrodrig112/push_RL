import random
import components
import itertools


class Player:
    """Class for one player in the Push game"""

    def __init__(self, name):
        """
        Players are initialized with the following:
            - Name (str): Name of the player
            - Score (int): Initial score of the player - always 0
            - Drawing (bool): Indicates whether the player is going to continue to draw or not

        Other attributes of players:
            - self.unbanked_cards = cards that are not banked
            - self.banked_cards = cards that are banked (safe from push roles)
            - self.pushed = Did the player just push
        """
        self.name = name
        self.drawing = True
        self.score = 0
        self.unbanked_cards = {'Red': [], 'Blue': [], 'Yellow': [], 'Green': [], 'Purple': []}
        self.banked_cards = {'Red': [], 'Blue': [], 'Yellow': [], 'Green': [], 'Purple': []}
        self.pushed = False

    # Begin turn taking methods - likely will end up as sub-functions within a method
    def select_pile_for_card(self, available_piles):
        """ Given an active card and set of piles to play to, randomly place the card in a pile"""
        if available_piles:
            selection = random.choice(available_piles)
            return selection
        else:
            self.pushed = True
            return None

    def draw_or_pass(self):
        """ Randomly decide whether or not to continue drawing or to pass"""
        self.drawing = random.choice([True, False])

    def push(self, game):
        """Randomly select a set of unbanked cards to remove"""
        print(f"{self.name} has to push!")
        roll = game.dice.roll()
        print("Push roll: {}".format(roll))
        if roll:
            self.unbanked_cards[roll] = []

    def collect_card_pile(self, game):
        """ Collect a pile from the center and add cards (excluding bombs and reverse) to unbanked"""
        selection = random.choice(game.piles)
        for card in selection.card_stack:
            if card.color in game.colors:  # don't add bombs or reverse
                self.unbanked_cards[card.color].append(card.number)
            elif card.color == "Bomb":
                self.push(game)
        game.piles.remove(selection)
        return selection

    def update_score(self):
        banked_score = sum(itertools.chain.from_iterable(self.banked_cards.values()))
        unbanked_score = sum(itertools.chain.from_iterable(self.unbanked_cards.values()))
        self.score = banked_score + unbanked_score

    def reset(self):
        """ Ensure that the player begins their turn on a clean slate"""
        self.drawing = True
        self.pushed = False

    def __str__(self):
        return "{name}: {score} points".format(name=self.name, score=self.score)


class PushGame:
    """Class for the Push Game"""

    def __init__(self, players, deck, dice):
        """
        PushGames are initialized with the following
        :param
            players (list): Players involved in game in turn order)
            deck (list): Stack of cards representing the deck
            piles (list of lists): Piles the active card is played into
            active_card (card): The card most recently drawn off the deck
            available_piles (list): indices of the piles the active card can be played into
            piles_for_collection (list): list of piles that players can choose to collect from
            players_to_collect (list): players who will be picking up piles from the center

            running (bool): Indicator for whether game is currently in motion

            winners (list): Winner(s) of the game
            top_score (int): Winning score


        """
        self.players = players
        self.num_players = len(players)
        self.deck = deck
        self.dice = dice
        self.colors = ['Red', 'Blue', 'Yellow', 'Green', 'Purple']
        self.running = False
        self.piles = [components.Pile(None), components.Pile(None), components.Pile(None)]
        self.active_card = None
        self.available_piles = []
        self.piles_for_collection = []
        self.players_to_collect = []
        self.current_player = None
        self.direction = 1

        self.winners = None
        self.top_score = None

    def identify_playable_piles(self):
        self.available_piles = []
        for pile_index in range(len(self.piles)):
            if self.piles[pile_index].check_availability(self.active_card):
                self.available_piles.append(pile_index)

    def switch_play_direction(self):
        self.direction = self.direction * -1

    def win(self):
        """Return the player(s) with the highest score in the game"""
        score_dictionary = {player.name: player.score for player in self.players}
        self.top_score = max(score_dictionary.values())
        winners = [player for player, score in score_dictionary.items() if score == self.top_score]
        self.winners = winners

    def reset(self, player):
        player.reset()
        self.piles = self.piles = [components.Pile([]), components.Pile([]), components.Pile([])]
        self.available_piles = [0, 1, 2]
        self.piles_for_collection = []

    def check_piles_for_collection(self):
        """ Identify piles with 1 or more cards that players can collect """
        for pile in self.piles:
            if pile.count_cards() >= 1:
                self.piles_for_collection.append(pile)

    def get_players_to_collect(self, player):
        initial_indices = [self.current_player + i for i in range(3)]
        if player.pushed:
            initial_indices = [i + 1 for i in initial_indices]
        self.players_to_collect = [i % self.num_players for i in initial_indices]
        print(self.players_to_collect)

    def players_collect_piles(self, player):
        self.get_players_to_collect(player)
        for j in self.players_to_collect:
            player_to_collect = self.players[j]
            self.check_piles_for_collection()
            collection = player_to_collect.collect_card_pile(self)
            player_to_collect.update_score()
            print(f"{player_to_collect.name} collects pile {collection}")
            print(player_to_collect)

    def play(self):
        """Play the game"""
        self.running = True
        while self.running:  # While in running state...
            for i in range(len(self.players)):  # ...players each take their turn...
                self.current_player = i
                player = self.players[i]
                if self.running:
                    self.reset(player)  # ... beginning by drawing at least one card onto the empty piles.
                    while player.drawing:  # On their turn a player will draw cards
                        if self.deck.count_cards() > 0:  # assuming there are cards left
                            self.active_card = self.deck.draw()
                            print(f"{player.name} draws a {self.active_card}")
                            if self.active_card.color == "Reverse":
                                self.switch_play_direction()
                            else:
                                self.identify_playable_piles()
                                selection = player.select_pile_for_card(self.available_piles)  # select a
                                # location for the drawn card
                                if player.pushed:
                                    player.drawing = False
                                    player.push(self)
                                else:
                                    self.piles[selection].add_card_to_stack(self.active_card)  # and then place it
                                    player.draw_or_pass()  # ... until the player decides not to draw anymore and ends
                                    # their turn.

                                print(f"Its placed in pile {selection}, ({self.available_piles} were available)")
                                print(f"{self.deck.count_cards()} cards remain")
                            if not player.drawing:  # once the player is done drawing, they pick a pile and update
                                # their score
                                self.players_collect_piles(player)
                                print("")
                                if self.deck.count_cards() == 0:
                                    self.running = False
                        elif self.deck.count_cards() == 0:  # The game ends once the deck is empty
                            self.running = False
                            player.drawing = False
                            self.players_collect_piles(player)
                            print('The game is over, there are no more cards')
                            print('')
        # Once the deck is out of cards, determine a winner
        self.win()
        if len(self.winners) == 1:  # If there is a single winner
            print("{winner} wins the game with a score of {score}".format(winner=self.winners[0], score=self.top_score))
        else:  # print the multiple winners
            print("{winners} tied for first with a score of {score}".format(winners=" and ".join(self.winners),
                                                                            score=self.top_score))
