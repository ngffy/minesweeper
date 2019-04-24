#!/usr/bin/env python3

import pygame
import tkinter
from tkinter import messagebox
import sys
from pygame.locals import *
from square import Square
from board import Board

def make_board(rows, cols, mines):
    pygame.init()

    # Pygame/ALSA has a bug that results in high CPU usage. This line reduces
    # the CPU usage
    pygame.mixer.quit()

    DISPLAYSURF = pygame.display.set_mode((1280, 720))
    DISPLAYSURF.fill((185,185,185))
    pygame.display.set_caption("Minesweeper")

    # Prevents mouse movement from counting as an event, reducing CPU usage
    pygame.event.set_blocked(MOUSEMOTION)

    return Board((rows, cols), mines, DISPLAYSURF)

def play_game(rows, cols, mines):
    board = make_board(rows, cols, mines)

    # Creates an event that will cause the board timer to update every 100ms
    UPDATETIMER = pygame.USEREVENT + 1
    pygame.time.set_timer(UPDATETIMER, 100)

    while True:
        board.check_for_win()
        pygame.display.update()

        if board.game_lost or board.game_won:
            break

        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == UPDATETIMER:
            board.update_timer()
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            if not board.game_started:
                board.place_mines(event.pos)
            board.left_click(event.pos)
        elif event.type == MOUSEBUTTONUP and event.button == 3:
            board.right_click(event.pos)

def inputs_are_valid(rows, cols, mines):
    if not (5 <= rows <= 99) or not (5 <= cols <= 99):
        messagebox.showerror("Input Error",
                "Rows and columns must be between 5 and 99")
        return False

    if not (1 <= mines):
        messagebox.showerror("Input Error", "There must be at least one mine")
        return False

    # 9 is subtracted because the player's first click will clear a minimum of
    # 9 spaces if not clicked on the board edge
    max_mines = rows * cols - 9
    if mines > max_mines:
        messagebox.showerror("Input Error",
                "Board is too small for this many mines!")
        return False

    return True

def ask_to_play_again():
    play_again_box = tkinter.Tk()
    question = tkinter.Label(play_again_box, text="Play again?")
    question.pack(side=tkinter.TOP)

    # Yes will destroy this Tk box and consequently reopen the option_box
    yes = tkinter.Button(play_again_box, text="Yes",
            command=play_again_box.destroy)
    yes.pack(side=tkinter.LEFT)

    # No will end the program
    no = tkinter.Button(play_again_box, text="No", command=sys.exit)
    no.pack(side=tkinter.RIGHT)

    play_again_box.mainloop()

def play_pressed(option_box):
    try:
        rows = int(option_box.children['!frame'].children['!spinbox'].get())
        cols = int(option_box.children['!frame2'].children['!spinbox'].get())
        mines = int(option_box.children['!frame3'].children['!spinbox'].get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter whole numbers!")
        return

    if inputs_are_valid(rows, cols, mines):
        option_box.destroy()
        play_game(rows, cols, mines)

        ask_to_play_again()

def add_option_for(var, lower, upper, window):
    frame = tkinter.Frame(window)
    frame.pack()
    label = tkinter.Label(frame, text=var + ":")
    label.pack(side=tkinter.LEFT)
    val = tkinter.Spinbox(frame, from_=lower, to=upper, width=len(str(upper)))
    val.pack(side=tkinter.LEFT)

def main():
    while True:
        option_box = tkinter.Tk()

        add_option_for("Rows", 5, 99, option_box)
        add_option_for("Columns", 5, 99, option_box)
        add_option_for("Mines", 1, 9801, option_box)

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
