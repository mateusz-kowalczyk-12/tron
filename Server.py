import json
import Constants as Cs

from Game import Game
from socket import socket, AF_INET,  SOCK_STREAM
from threading import Thread, Lock
from time import sleep
import pickle

HOST = '127.0.0.1'
PORT = Cs.PORT
TICKRATE = 30


def handler(conn, player_ix, lock):
    conn.sendall(str(player_ix).encode() if player_ix is not None else "LOBBY FULL")

    while True:
        sleep(1 / TICKRATE)
        lock.acquire()
        if game.state == Cs.State.WAITING:
            lock.release()
            print(f'state: {game.state}')
            conn.sendall(json.dumps(game.get_active_players_n()).encode())
        elif game.state == Cs.State.IN_PROGRESS:
            lock.release()
            move = conn.recv(256).decode()  # LEFT/RIGHT
            game.make_move(player_ix, json.loads(move))
        elif game.state == Cs.State.END:
            lock.release()
            conn.sendall("tutaj dodac kto wygral".encode())
            conn.shutdown()
            game.remove_player()
            break


if __name__ == '__main__':
    game = Game()
    player_sockets = []

    lock = Lock()

    server = socket(AF_INET, SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    thread = None
    ready = False
    while True:
        if game.state == Cs.State.WAITING:
            conn, _ = server.accept()
            print("accepted")
            player_sockets.append(conn)
            thread = Thread(target=handler, args=(conn, game.add_player(), lock))
            thread.start()
            if game.connected_players_n == Cs.MAX_CONNECTED_PLAYERS_N:


                lock.acquire()
                print('is hererere')
                game.state = Cs.State.IN_PROGRESS
                lock.release()
                sleep(1)

        elif game.state == Cs.State.IN_PROGRESS:
            sleep(1 / TICKRATE)
            for i, conn in enumerate(player_sockets):
                if not game.is_playing[i]:
                    conn.sendall("GAME OVER".encode())
                else:
                    print(f'Sending board: {game.get_board().fields_colors}')
                    conn.sendall(pickle.dumps(game.get_board().fields_colors))
        elif game.state == Cs.State.IN_PROGRESS:
            pass
    thread.join()
