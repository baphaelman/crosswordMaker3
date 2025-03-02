from Board import Board
from Square import *

class Crossword:
    # ATTRIBUTES
    # r, c: number of rows and columns respectively
    # start_squares: list of Squares for row words to start at

    # INIT
    # dimensions: [row, col] list
    # blocks: list of Squares that correspond to black squares
    def __init__(self, dimensions, blocks):
        self.r, self.c = dimensions[0], dimensions[1]
        self.template_board = Board(dimensions, blocks)