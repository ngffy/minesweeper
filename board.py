import pygame
import random
from square import Square

class Board:
    def __init__(self, size, square_size, surface):
        self.surface = surface
        self.size = size
        self.square_size = square_size
        self.game_lost = False
        self.game_won = False
        self.total_flags = 0
        self.coords = (0,50)

        self.unclicked_squares = size[0] * size[1]
        self.total_mines = round(.2*self.unclicked_squares)

        # Makes a 2D list of Square objects
        start_x = self.coords[0]
        start_y = self.coords[1]
        end_x = start_x + self.square_size*size[1]
        end_y = start_y + self.square_size*size[0]
        self.squares = [[Square(self, i, j)
            for i in range(start_x, end_x, self.square_size)]
            for j in range(start_y, end_y, self.square_size)] 

        # Font object for mine counter and timer
        self.game_font = pygame.font.Font('freesansbold.ttf', 48)

    def update_mine_counter(self):
        # Makes the mine counter the right size
        self.mine_counter = self.game_font.render("99", True, (255,0,0))
        self.counter_loc = self.mine_counter.get_rect()
        self.counter_loc.bottomleft = self.coords

        # Makes the background of the counter black
        self.mine_counter.fill((0,0,0))
        self.surface.blit(self.mine_counter, self.counter_loc)

        mines_left = str(self.total_mines - self.total_flags)
        if len(mines_left) == 1:
            mines_left = "0" + mines_left
        self.mine_counter = self.game_font.render(mines_left, True, (255,0,0))
        self.counter_loc = self.mine_counter.get_rect()
        self.counter_loc.bottomleft = self.coords
        self.surface.blit(self.mine_counter, self.counter_loc)

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
                sx, sy = s.coords
                too_far_right = sx+self.square_size < mousex
                too_far_up = sy+self.square_size < mousey
                too_far_down = sy > mousey
                if not (too_far_right or too_far_up or too_far_down):
                    return s
        return None

    def get_index(self, s):
        for row in self.squares:
            if s in row:
                return (self.squares.index(row), row.index(s))

    # Places mines in such a way that the first space clicked will be a 0 space
    # Returns False if a mine was clicked, returns True otherwise
    def place_mines(self, mousepos):
        square = self.get_clicked_square(mousepos)
        if square is None:
            return True
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
        return False

    def squares_adjacent_to(self, s):
        x, y = self.get_index(s)
        adj_indices = [(x-1,y-1), (x,y-1), (x+1,y-1),
                (x-1,y), (x+1,y),
                (x+1,y+1), (x,y+1), (x-1,y+1)]
        adj_squares = [self.squares[i[0]][i[1]] for i in adj_indices 
            if 0 <= i[0] < self.size[0] and 0 <= i[1] < self.size[1]]
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
