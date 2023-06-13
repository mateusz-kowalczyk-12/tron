import json
import pickle
from threading import Thread
import socket

import Constants as Cs
from Move import Move
from UI import UI


class Client:
    def __init__(self):
        self.color = None
        self.socket = None
        self.UI = UI()

        while True:
            self.UI.display_menu()
            self.connect_to_server()
            server_communication_thread = Thread(target=self.communicate_with_server)
            server_communication_thread.start()
            self.UI.display_waiting_room()
            self.UI.display_board()
            break

        server_communication_thread.join()

    def communicate_with_server(self):
        while True:
            try:
                connected_players_n = int(self.socket.recv(256).decode())
            except Exception:
                connected_players_n = Cs.MAX_CONNECTED_PLAYERS_N

            self.UI.lock.acquire()
            self.UI.connected_players_n = connected_players_n
            self.UI.lock.release()

            if connected_players_n == Cs.MAX_CONNECTED_PLAYERS_N:
                break

        while True:
            if self.UI.current_direction is not None:
                self.socket.sendall(str(self.UI.current_direction).encode())

            data_received = self.socket.recv(4096)
            if data_received == "GAME OVER".encode():
                break
            elif data_received == b'3':
                print('Skipping')
            else:
                print(data_received)
                try:
                    new_fields_colors = pickle.loads(data_received)
                    print(new_fields_colors)
                    self.UI.fields_colors = new_fields_colors
                except Exception:
                    pass

    def connect_to_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('127.0.0.1', Cs.PORT))
        self.color = int(self.socket.recv(256).decode())
        print(f"Received color {self.color}")

    def send_move(self, move: Move):
        self.socket.send(json.dumps(move).encode())


client = Client()
