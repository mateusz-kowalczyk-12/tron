from enum import Enum

import numpy as np

BOARD_WIDTH = 32
BOARD_HEIGHT = 32
DIRECTIONS_N = 4
MAX_CONNECTED_PLAYERS_N = 2
PORT = 2138

COLORS = {
    0: (255, 0, 0),
    1: (0, 255, 0),
    2: (0, 0, 255),
    3: (0, 0, 0),
    4: (255, 255, 255)
}
SCOLORS = {
    'RED': COLORS[0],
    'GREEN': COLORS[1],
    'BLUE': COLORS[2],
    'BLACK': COLORS[3],
    'WHITE': COLORS[4]
}


class State(Enum):
    WAITING = 0
    IN_PROGRESS = 1
    END = 2
