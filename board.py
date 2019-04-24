import pygame
import random
import time
from square import Square

class Board:
    def __init__(self, size, mines, surface, square_size=40):
        self.surface = surface
        self.size = size
        self.square_size = square_size
        self.game_lost = False
        self.game_won = False
        self.total_flags = 0
        self.game_started = False

        self.unclicked_squares = size[0] * size[1]
        self.total_mines = mines

        len_x = self.square_size*size[1]
        len_y = self.square_size*size[0]
        self.square_grid = pygame.Rect(0, 50, len_x, len_y)

        # Makes a 2D list of Square objects
        start_x, start_y = self.square_grid.topleft
        end_x, end_y = self.square_grid.bottomright
        self.squares = [[Square(self, i, j)
            for i in range(start_x, end_x, self.square_size)]
            for j in range(start_y, end_y, self.square_size)] 

        # Font object for mine counter and timer
        self.game_font = pygame.font.Font('freesansbold.ttf', 48)

        # Places the mine counter
        self.mine_counter = self.game_font.render(str(mines), True, (255,0,0))
        self.counter_loc = self.mine_counter.get_rect()
        self.counter_loc.bottomleft = self.square_grid.topleft
        self.update_mine_counter()

        # Places the timer
        self.timer = self.game_font.render("999", True, (255,0,0))
        self.timer_loc = self.timer.get_rect()
        self.timer_loc.bottomright = self.square_grid.topright

        self.start_time = 0
        self.curr_time = 0

    def update_mine_counter(self):
        # Makes the background of the counter black
        self.mine_counter.fill((0,0,0))
        self.surface.blit(self.mine_counter, self.counter_loc)

        mines_left = str(self.total_mines - self.total_flags)

        # Pads with zeroes
        max_digits = len(str(self.total_mines))
        mines_left = "0"*(max_digits-len(mines_left)) + mines_left

        self.mine_counter = self.game_font.render(mines_left, True, (255,0,0))
        self.surface.blit(self.mine_counter, self.counter_loc)

    def update_timer(self):
        # Makes the background of the timer black
        self.timer.fill((0,0,0))
        self.surface.blit(self.timer, self.timer_loc)

        if self.game_started:
            self.curr_time = time.time()
            time_elapsed = str(round(self.curr_time - self.start_time))
            time_elapsed = "0"*(3-len(time_elapsed)) + time_elapsed
        else:
            time_elapsed = "000"

        if len(time_elapsed) > 3:
            time_elapsed = "999"

        self.timer = self.game_font.render(time_elapsed, True, (255,0,0))
        self.surface.blit(self.timer, self.timer_loc)

    def check_for_win(self):
        only_mines_left = self.total_mines == self.unclicked_squares
        if not self.game_lost and only_mines_left:
            self.game_won = True
            self.flag_remaining_mines()

    def show_unflagged_mines(self):
        for row in self.squares:
            for s in row:
                if s.is_mine and not s.is_flagged:
                    s.reveal()
                elif not s.is_mine and s.is_flagged:
                    s.draw_line()

    def flag_remaining_mines(self):
        for row in self.squares:
            for s in row:
                if s.is_mine and s.is_questioned:
                    s.cycle_flag()
                if s.is_mine and not s.is_flagged:
                    s.cycle_flag()

    def get_clicked_square(self, mousepos):
        mousex, mousey = mousepos
        for row in self.squares:
            for s in row:
                too_far_right = mousex > s.dimensions.right
                too_far_up = mousey < s.dimensions.top
                too_far_down = mousey > s.dimensions.bottom
                if not (too_far_right or too_far_up or too_far_down):
                    return s
        return None

    def get_index(self, s):
        for row in self.squares:
            if s in row:
                return (self.squares.index(row), row.index(s))

    # Places mines in such a way that the first space clicked will be a 0 space
    # Also starts timer
    def place_mines(self, mousepos):
        square = self.get_clicked_square(mousepos)
        if square is None:
            return
        adj_squares = self.squares_adjacent_to(square)
        free_spaces = self.unclicked_squares-self.total_mines-1-len(adj_squares)
        is_mine = ([True]*self.total_mines + [False]*free_spaces)
        random.shuffle(is_mine)
        for row in self.squares:
            for s in row:
                if s is not square and s not in adj_squares:
                    s.is_mine = is_mine.pop()
        for row in self.squares:
            for s in row:
                adj_squares = self.squares_adjacent_to(s)
                total_adj_mines = sum([i.is_mine for i in adj_squares])
                s.mines_touching = total_adj_mines
        self.start_time = time.time()
        self.game_started = True

    def squares_adjacent_to(self, s):
        i, j = self.get_index(s)
        adj_indices = [(i-1,j-1), (i,j-1), (i+1,j-1),
                (i-1,j), (i+1,j),
                (i-1,j+1), (i,j+1), (i+1,j+1)]
        adj_squares = [self.squares[i][j] for i, j in adj_indices
            if 0 <= i < self.size[0] and 0 <= j < self.size[1]]
        return adj_squares

    def open(self, s):
        if s.is_clicked or s.is_flagged:
            return
        s.reveal()
        if s.is_clicked:
            self.unclicked_squares -= 1
        if s.is_mine and s.is_clicked:
            self.game_lost = True
            self.show_unflagged_mines()
        elif not s.is_mine and s.is_clicked and s.mines_touching == 0:
            self.open_squares_adjacent_to(s)

    def open_squares_adjacent_to(self, square):
        adj_squares = self.squares_adjacent_to(square)
        counter = 0
        for s in adj_squares:
            if s.is_flagged:
                counter += 1
        if counter != square.mines_touching:
            return
        for s in adj_squares:
            self.open(s)

    def left_click(self, mousepos):
        square = self.get_clicked_square(mousepos)
        if square is None:
            return
        elif square.is_clicked:
            self.open_squares_adjacent_to(square)
            return
        self.open(square)

    def right_click(self, mousepos):
        square = self.get_clicked_square(mousepos)
        if square is None:
            return
        square.cycle_flag()
        if square.is_flagged:
            self.total_flags += 1
        elif square.is_questioned:
            self.total_flags -= 1
        self.update_mine_counter()
