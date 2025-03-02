from Board import Board
from Square import *

class Crossword:
    # ATTRIBUTES
    # r, c: number of rows and columns respectively
    # template_board: board with #, StartSquares, and characters as requested

    # INIT
    # dimensions: [row, col] list
    # blocks: list of Squares that correspond to black squares
    # needed_words: list of strings that must be included (anywhere)
    # specified_chars: dictionary with key Squares of characters whose position was specifically requested
    def __init__(self, dimensions, blocks, needed_words, specified_chars):
        self.r, self.c = dimensions[0], dimensions[1]
        self.template_board = Board(dimensions, blocks, specified_chars)
        self.needed_words = needed_words

