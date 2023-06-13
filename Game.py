from enum import Enum

from Move import Move
from Board import Board
import Constants as Cs
import functools
import threading


def synchronized(wrapped):
    lock = threading.Lock()

    @functools.wraps(wrapped)
    def _wrap(*args, **kwargs):
        with lock:
            return wrapped(*args, **kwargs)

    return _wrap


class Game:
    def __init__(self):
        self.state = Cs.State.WAITING
        self.connected_players_n = 0
        self.board = Board((Cs.BOARD_HEIGHT, Cs.BOARD_WIDTH))
        self.player_pos = [
            (10, 7),
            (31, 10),
            (0, 16),
        ]

        self.player_dir = [
            (1, 0),
            (-1, 0),
            (0, -1)
        ]

        self.is_playing = [
            False,
            False,
            False
        ]

    @synchronized
    def add_player(self):
        if self.connected_players_n == Cs.MAX_CONNECTED_PLAYERS_N:
            return None
        self.connected_players_n += 1
        self.is_playing[self.connected_players_n - 1] = True
        return self.connected_players_n - 1

    @synchronized
    def make_move(self, player_no, move):
        dir = self.player_dir[player_no]
        print("tutaj")
        if move == Move.LEFT:
            self.player_dir[player_no] = [dir[1], -1 * dir[0]]
        elif move == Move.RIGHT:
            self.player_dir[player_no] = [-1 * dir[1], dir[0]]

    @synchronized
    def move_forward(self):
        for p_no in range(0, self.connected_players_n):
            if not self.is_playing[p_no]:
                continue

            new_pos = (self.player_pos[p_no][0] + self.player_dir[p_no][0],
                       self.player_pos[p_no][1] + self.player_dir[p_no][1])


            if new_pos[0] >= self.board.dimensions[0] or new_pos[1] >= self.board.dimensions[1] \
                    or new_pos[0] < 0 or new_pos[1] < 0:
                self.is_playing[p_no] = False
                return

            new_pos_color = self.board.fields_colors[new_pos[0]][new_pos[1]]

            if new_pos_color != Cs.SCOLORS["BLACK"]:
                self.is_playing[p_no] = False

            self.player_pos[p_no] = new_pos
            self.board.fields_colors[new_pos[0]][new_pos[1]] = Cs.COLORS[p_no]

    @synchronized
    def get_board(self):
        return self.board

    @synchronized
    def get_state(self):
        return self.state

    @synchronized
    def set_state(self, state):
        self.state = state

    @synchronized
    def game_started(self):
        return self.state == Cs.State.IN_PROGRESS

    @synchronized
    def get_active_players_n(self):
        return self.connected_players_n
