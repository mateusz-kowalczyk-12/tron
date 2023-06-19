import json
import sys
import Constants as Cs

from Game import Game
from socket import socket, AF_INET,  SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread, Lock
from time import sleep
import pickle

HOST = '127.0.0.1'
PORT = Cs.PORT
TICKRATE = 10


def handler(conn, player_ix, game):
    conn.sendall(str(player_ix).encode() if player_ix is not None else "LOBBY FULL")

    while True:
        sleep(1 / TICKRATE)
        if game.get_state() == Cs.State.WAITING:
            conn.sendall(json.dumps(game.get_active_players_n()).encode())
        elif game.get_state() == Cs.State.IN_PROGRESS:
            try:
                move = conn.recv(256).decode()  # LEFT/RIGHT
                game.make_move(player_ix, json.loads(move))
            except Exception:
                break


class Server:
    def __init__(self):
        self.player_sockets = []
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.bind((HOST, PORT))
        self.game = Game()

    def run_in_progress(self):
        sleep(1 / TICKRATE)
        self.game.move_forward()
        any_playing = False
        for i, conn in enumerate(self.player_sockets):
            if not self.game.is_playing[i]:
                if sum([1 if i else 0
                        for i in self.game.is_playing]) > 0:
                    conn.sendall("GAME OVER".encode())
                else:
                    conn.sendall("GAME WON".encode())
            else:
                any_playing = True
                conn.sendall(pickle.dumps(self.game.get_board().fields_colors))

        if not any_playing:
            self.game.state = Cs.State.END
            for conn in self.player_sockets:
                conn.close()

    def run_waiting(self):
        conn, _ = self.socket.accept()
        self.player_sockets.append(conn)
        thread = Thread(target=handler, args=(conn, self.game.add_player(), self.game))
        thread.start()
        if self.game.connected_players_n == Cs.MAX_CONNECTED_PLAYERS_N:
            self.game.set_state(Cs.State.IN_PROGRESS)
            for conn in self.player_sockets:
                conn.sendall("START".encode())

    def run(self):
        self.socket.listen()
        while True:
            state = self.game.get_state()

            if state == Cs.State.WAITING:
                self.run_waiting()
            if state == Cs.State.IN_PROGRESS:
                self.run_in_progress()







if __name__ == '__main__':

    server = Server()
    server.run()

    # game = Game()
    # player_sockets = []

    # server = socket(AF_INET, SOCK_STREAM)
    # server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # server.bind((HOST, PORT))
    # server.listen()
    # thread = None
    # ready = False
    # while True:
    #     if game.get_state() == Cs.State.WAITING:
    #         conn, _ = server.accept()
    #         player_sockets.append(conn)
    #         thread = Thread(target=handler, args=(conn, game.add_player()))
    #         thread.start()
    #         if game.connected_players_n == Cs.MAX_CONNECTED_PLAYERS_N:
    #             game.set_state(Cs.State.IN_PROGRESS)
    #             sleep(1)
    #
    #     elif game.get_state() == Cs.State.IN_PROGRESS:
    #         sleep(1 / TICKRATE)
    #         game.move_forward()
    #         any_playing = False
    #         for i, conn in enumerate(player_sockets):
    #             if not game.is_playing[i]:
    #                 conn.sendall("GAME OVER".encode())
    #             else:
    #                 any_playing = True
    #                 conn.sendall(pickle.dumps(game.get_board().fields_colors))
    #
    #         if not any_playing:
    #             game.state = Cs.State.END
    #             for conn in player_sockets:
    #                 conn.close()
