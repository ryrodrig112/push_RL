import random
import strategies


class Player():
    """Class for one player in the Push game"""
    def __init__(self, name):
        """
        Players are initialized with the following:
            - Name (str): Name of the player
            - Score (int): Initial score of the player - always 0
        """
        self.name = name
        self.score = 0

    def __str__(self):
        return "{name}: {score} points".format(name=self.name, score=self.score)


class PushGame():
    """Class for the Push Game"""
    def __init__(self, players, deck):
        """
        PushGames are initialized with the following
        :param
            players (list): Players involved in game in turn order)
            deck (list): Stack of cards representing the deck
            running (bool): Indicator identifying whether game is currently in motion
        """
        self.players = players
        self.deck = deck
        self.running = False

    def play(self):
        """Play the game"""
        self.running = True
        while self.running:  # While we are playing the game, each player takes their turn in order
            for player in self. players:
                print(player)


