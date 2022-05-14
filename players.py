import random
import strategies

class Player:
    def __init__(self, strategy, points):
        self.strategy = strategy
        self.points = points

class Players():
    def __init__(self, players, order):
        self.players = players
        self.order = order
