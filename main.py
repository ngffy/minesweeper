import pygame
import sys
from pygame.locals import *
from square import Square
from board import Board

pygame.init()
# Pygame/ALSA has a bug that results in high CPU usage. This line reduces the
# CPU usage
pygame.mixer.quit()

DISPLAYSURF = pygame.display.set_mode((1280, 720))
DISPLAYSURF.fill((185,185,185))
pygame.display.set_caption("Minesweeper")

board = Board((16, 31), 40, DISPLAYSURF)
# board = Board((9, 10), 48, DISPLAYSURF)

# Prevents mouse movement from counting as an event, reducing CPU usage
pygame.event.set_blocked(MOUSEMOTION)

while True:
    board.update_mine_counter()
    board.update_timer()
    board.check_for_win()
    pygame.display.update()

    # TODO: Add options to play again
    if board.game_lost:
        print("You lose")
        break
    elif board.game_won:
        print("You win")
        break

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            if not board.game_started:
                board.place_mines(event.pos)
            board.left_click(event.pos)
        elif event.type == MOUSEBUTTONUP and event.button == 3:
            board.right_click(event.pos)
