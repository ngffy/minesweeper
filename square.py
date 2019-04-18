import pygame

class Square:
    def __init__(self, board, x, y):
        self.board = board
        self.surface = board.surface
        self.size = board.square_size

        self.is_clicked = False
        self.is_mine = False
        self.is_flagged = False
        self.is_questioned = False

        self.mines_touching = 0
        self.dimensions = pygame.Rect(x, y, self.size, self.size)
        self.set_img("png/Minesweeper_unopened_square.png")

    def draw_line(self):
        RED = (255,0,0)
        topleft = self.dimensions.topleft
        bottomright = self.dimensions.bottomright
        pygame.draw.line(self.surface, RED, topleft, bottomright, 10)

    def update_img(self):
        if self.is_mine:
            self.set_img("png/bomb.png")
        elif self.mines_touching == 0:
            self.set_img("png/Minesweeper_0.png")
        elif self.mines_touching == 1:
            self.set_img("png/Minesweeper_1.png")
        elif self.mines_touching == 2:
            self.set_img("png/Minesweeper_2.png")
        elif self.mines_touching == 3:
            self.set_img("png/Minesweeper_3.png")
        elif self.mines_touching == 4:
            self.set_img("png/Minesweeper_4.png")
        elif self.mines_touching == 5:
            self.set_img("png/Minesweeper_5.png")
        elif self.mines_touching == 6:
            self.set_img("png/Minesweeper_6.png")
        elif self.mines_touching == 7:
            self.set_img("png/Minesweeper_7.png")
        elif self.mines_touching == 8:
            self.set_img("png/Minesweeper_8.png")

    def set_img(self, img):
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, (self.size, self.size))
        self.surface.blit(self.img, self.dimensions.topleft)

    def reveal(self):
        if not self.is_flagged and not self.is_clicked:
            self.is_clicked = True
            self.is_questioned = False
            self.update_img()

    def cycle_flag(self):
        if self.is_clicked:
            return
        elif self.is_flagged:
            self.set_img("png/Minesweeper_questionmark.png")
            self.is_flagged = False
            self.is_questioned = True
        elif self.is_questioned:
            self.set_img("png/Minesweeper_unopened_square.png")
            self.is_questioned = False
        else:
            self.set_img("png/Minesweeper_flag.png")
            self.is_flagged = True
