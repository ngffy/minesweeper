#!/usr/bin/env python3

import pygame
import tkinter
from tkinter import messagebox
import sys
from pygame.locals import *
from square import Square
from board import Board

def start_game(rows, cols, mines):
    pygame.init()
    # Pygame/ALSA has a bug that results in high CPU usage. This line reduces
    # the CPU usage
    pygame.mixer.quit()

    DISPLAYSURF = pygame.display.set_mode((1280, 720))
    DISPLAYSURF.fill((185,185,185))
    pygame.display.set_caption("Minesweeper")

    board = Board((rows, cols), mines, DISPLAYSURF)

    # Prevents mouse movement from counting as an event, reducing CPU usage
    pygame.event.set_blocked(MOUSEMOTION)

    while True:
        board.update_mine_counter()
        board.update_timer()
        board.check_for_win()
        pygame.display.update()

        if board.game_lost or board.game_won:
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

def play_pressed(option_box):
    try:
        row_input = int(option_box.children['!frame'].children['!spinbox'].get())
        col_input = int(option_box.children['!frame2'].children['!spinbox'].get())
        mine_input = int(option_box.children['!frame3'].children['!spinbox'].get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter whole numbers!")
        return

    if not (5 <= row_input <= 99) or not (5 <= col_input <= 99):
        messagebox.showerror("Input Error",
                "Rows and columns must be between 5 and 99")
        return

    if not (1 <= mine_input):
        messagebox.showerror("Input Error", "There must be at least one mine")
        return

    max_mines = row_input * col_input - 1
    if mine_input > max_mines:
        messagebox.showerror("Input Error",
                "Board is too small for this many mines!")
        return

    option_box.destroy()
    start_game(row_input, col_input, mine_input)

    # These lines will not execute until the game is over
    play_again_box = tkinter.Tk()
    question = tkinter.Label(play_again_box, text="Play again?")
    question.pack(side=tkinter.TOP)

    yes = tkinter.Button(play_again_box, text="Yes",
            command=play_again_box.destroy)
    yes.pack(side=tkinter.LEFT)

    no = tkinter.Button(play_again_box, text="No", command=sys.exit)
    no.pack(side=tkinter.RIGHT)

    play_again_box.mainloop()

def main():
    while True:
        option_box = tkinter.Tk()

        # Sets up row number input
        row_frame = tkinter.Frame(option_box)
        row_frame.pack()
        row_label = tkinter.Label(row_frame, text="Rows:")
        row_label.pack(side=tkinter.LEFT)
        rows = tkinter.Spinbox(row_frame, from_=5, to=99, width=2)
        rows.pack(side=tkinter.LEFT)

        # Sets up column number input
        col_frame = tkinter.Frame(option_box)
        col_frame.pack()
        col_label = tkinter.Label(col_frame, text="Columns:")
        col_label.pack(side=tkinter.LEFT)
        cols = tkinter.Spinbox(col_frame, from_=5, to=99, width=2)
        cols.pack(side=tkinter.LEFT)

        # Sets up mine number input
        # TODO: Set default number of mines (20% of board)
        mine_frame = tkinter.Frame(option_box)
        mine_frame.pack()
        mine_label = tkinter.Label(mine_frame, text="Mines:")
        mine_label.pack(side=tkinter.LEFT)
        mines = tkinter.Spinbox(mine_frame, from_=0, to=9800, width=4)
        mines.pack(side=tkinter.LEFT)

        # The lambda is so play_pressed(option_box) is not immediately executed
        # Otherwise the window will close early
        start_button = tkinter.Button(option_box, text="Play",
                command=lambda: play_pressed(option_box))
        start_button.pack()

        # Makes the program end if option_box's x button is pressed
        option_box.protocol("WM_DELETE_WINDOW", sys.exit)

        option_box.mainloop()

if __name__ == "__main__":
    main()
