from enum import Enum
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
            (1, 1),
            (0, 255, 0),
            (0, 0, 255)
        ]

        self.player_dir = [
            (1, 0),
            (0, -1),
            (-1, 0)
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
        self.player_dir[player_no] = move

    @synchronized
    def move_forward(self):
        for p_no in range(0, self.connected_players_n):
            if not self.is_playing[p_no]:
                continue

            new_pos = (self.player_pos[p_no][0] + self.player_pos[p_no][0],
                       self.player_pos[p_no][1] + self.player_pos[p_no][1])

            new_pos_color = self.board.fields_colors[new_pos[0]][new_pos[1]]
            if new_pos_color != Cs.COLORS[p_no] and new_pos_color != Cs.SCOLORS["BLACK"]:
                self.is_playing[p_no] = False
                for y in self.board.dimensions[0]:
                    for x in self.board.dimensions[1]:
                        if self.board.fields_colors[y][x] == Cs.COLORS[p_no]:
                             self.board.fields_colors = Cs.SCOLORS["BLACK"]

            self.player_pos[p_no] = new_pos

    @synchronized
    def get_board(self):
        return self.board

    @synchronized
    def game_started(self):
        return self.state == Cs.State.IN_PROGRESS

    @synchronized
    def get_active_players_n(self):
        return self.connected_players_n
