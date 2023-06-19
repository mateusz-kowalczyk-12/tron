import json

import pygame
import sys
import numpy as np
import threading
import Constants as Cs
import Move
from Direction import Direction


class UI:
    BOTTOM_BAR = 50
    WINDOW_HEIGHT = Cs.BOARD_HEIGHT * 16
    WINDOW_WIDTH = Cs.BOARD_WIDTH * 16

    BLACK = Cs.SCOLORS['BLACK']
    WHITE = Cs.SCOLORS['WHITE']

    def __init__(self, client):
        self.fields_colors = None
        self.SCREEN = pygame.display.set_mode((UI.WINDOW_WIDTH, UI.WINDOW_HEIGHT + UI.BOTTOM_BAR))

        self.connected_players_n = 0
        self.lock = threading.Lock()

        self.reset_data()
        self.client = client

    def reset_data(self):
        self.CLOCK = pygame.time.Clock()
        self.SCREEN.fill(UI.BLACK)
        self.fields_colors = [
            [Cs.SCOLORS['BLACK'] for _ in range(Cs.BOARD_WIDTH)]
            for _ in range(Cs.BOARD_HEIGHT)
        ]
        self.connected_players_n = 0

    def display_menu(self):
        pygame.init()
        self.SCREEN.fill(UI.BLACK)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('TRON', True, Cs.SCOLORS['GREEN'], Cs.SCOLORS['BLACK'])
        textRect = text.get_rect()
        textRect.center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2)

        font2 = pygame.font.Font('freesansbold.ttf', 32)
        text2 = font2.render('Wciśnij spację by dołączyć', True, Cs.SCOLORS['GREEN'], Cs.SCOLORS['BLACK'])
        textRect2 = text2.get_rect()
        textRect2.center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 30)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.K_SPACE:
                    return
            self.SCREEN.blit(text, textRect)
            self.SCREEN.blit(text2, textRect2)

            pygame.display.update()

    def display_waiting_room(self):
        fps_cap = 60
        clock = pygame.time.Clock()
        self.SCREEN.fill(UI.BLACK)

        while True:
            self.lock.acquire()
            if self.connected_players_n >= Cs.MAX_CONNECTED_PLAYERS_N:
                return
            self.lock.release()

            font = pygame.font.Font('freesansbold.ttf', 32)

            self.lock.acquire()
            text = font.render(f'Połączono {self.connected_players_n}/{Cs.MAX_CONNECTED_PLAYERS_N}',
                               True, Cs.SCOLORS['GREEN'], Cs.SCOLORS['BLACK'])
            self.lock.release()

            textRect = text.get_rect()
            textRect.center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2)
            font2 = pygame.font.Font('freesansbold.ttf', 32)
            text2 = font2.render(f'Oczekiwanie na pozostałych',
                                 True, Cs.SCOLORS['GREEN'], Cs.SCOLORS['BLACK'])
            textRect2 = text2.get_rect()
            textRect2.center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            clock.tick(fps_cap)
            self.SCREEN.blit(text2, textRect2)
            self.SCREEN.blit(text, textRect)
            pygame.display.flip()
            pygame.display.update()

    def display_count_down(self):
        fps_cap = 60
        clock = pygame.time.Clock()
        self.SCREEN.fill(UI.BLACK)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('A wygrał Pan Paweł', True, Cs.SCOLORS['GREEN'], Cs.SCOLORS['BLACK'])
        textRect = text.get_rect()
        textRect.center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2)

        font2 = pygame.font.Font('freesansbold.ttf', 32)
        text2 = font2.render('A wygrał Pan Paweł', True, Cs.SCOLORS['GREEN'], Cs.SCOLORS['BLACK'])
        textRect2 = text2.get_rect()
        textRect2.center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 30)

        while True:
            clock.tick(fps_cap)
            self.SCREEN.blit(text2, textRect)
            self.SCREEN.blit(text, textRect)
            pygame.display.flip()
            pygame.display.update()

    def display_board(self, client):
        fps_cap = 60
        clock = pygame.time.Clock()
        while self.client.is_game_won[0] is None:
            clock.tick(fps_cap)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    try:
                        client.socket.sendall(json.dumps(Move.Move.LEFT).encode())
                    except BrokenPipeError:
                        return

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    try:
                        client.socket.sendall(json.dumps(Move.Move.RIGHT).encode())
                    except BrokenPipeError:
                        return

            # self.lock.acquire()
            block_height = UI.WINDOW_HEIGHT // self.fields_colors.__len__()
            block_width = UI.WINDOW_WIDTH // self.fields_colors[0].__len__()
            # self.lock.release()
            
            ind_x = 0
            for x in range(0, UI.WINDOW_WIDTH, block_width):
                ind_y = 0
                for y in range(0, UI.WINDOW_HEIGHT, block_height):
                    rect = pygame.Rect(x, y, block_width, block_height)
                    # self.lock.acquire()
                    pygame.draw.rect(self.SCREEN, self.fields_colors[ind_x][ind_y], rect)
                    # self.lock.release()
                    ind_y += 1
                ind_x += 1
            pygame.display.flip()
            pygame.display.update()

    def display_game_over(self):
        pygame.init()
        self.SCREEN.fill(UI.BLACK)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Koniec gry', True, Cs.SCOLORS['GREEN'], Cs.SCOLORS['BLACK'])
        textRect = text.get_rect()
        textRect.center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2)

        font2 = pygame.font.Font('freesansbold.ttf', 32)
        text2 = font2.render('Przegrałeś', True, Cs.SCOLORS['GREEN'], Cs.SCOLORS['BLACK'])
        textRect2 = text2.get_rect()
        textRect2.center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 30)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.K_SPACE:
                    return
            self.SCREEN.blit(text, textRect)
            self.SCREEN.blit(text2, textRect2)

            pygame.display.update()

    def display_game_win(self):
        pygame.init()
        self.SCREEN.fill(UI.BLACK)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Koniec gry', True, Cs.SCOLORS['GREEN'], Cs.SCOLORS['BLACK'])
        textRect = text.get_rect()
        textRect.center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2)

        font2 = pygame.font.Font('freesansbold.ttf', 32)
        text2 = font2.render('Wygrałeś', True, Cs.SCOLORS['GREEN'], Cs.SCOLORS['BLACK'])
        textRect2 = text2.get_rect()
        textRect2.center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 30)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.K_SPACE:
                    return
            self.SCREEN.blit(text, textRect)
            self.SCREEN.blit(text2, textRect2)

            pygame.display.update()

