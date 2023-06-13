import Constants as Cs
from Direction import Direction

import random


class Player:
    def __init__(self, color: int, position: (int, int)):
        self.color: int = color
        self.position: (int, int) = position
        self.direction: Direction = Direction(random.randint(0, Cs.DIRECTIONS_N))
        self.is_alive: bool = True

    def change_position(self, new_position):
        self.position = new_position
