import Constants as Cs
import numpy as np


class Board:
    def __init__(self, dimensions: (int, int)):
        self.dimensions = dimensions
        self.fields_colors: [int, int] = [
            [Cs.SCOLORS['BLACK'] for _ in range(Cs.BOARD_WIDTH)]
            for _ in range(Cs.BOARD_HEIGHT)
        ]

    def update_board(self):
        pass

    def clear(self):
        self.fields_colors = [
            [Cs.SCOLORS['BLACK'] for _ in range(Cs.BOARD_WIDTH)]
            for _ in range(Cs.BOARD_HEIGHT)
        ]
