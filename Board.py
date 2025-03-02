from Square import *

class Board:
    # ATTRIBUTES
    # r, c: number of rows and columns, respectively
    # grid: rxc matrix of Squares
    # row_start_squares: list of row start squares, ordered by row then column (increasing)
    # col_start_squares: list of col start squares

    def __init__(self, dimensions, blocks):
        self.r, self.c = dimensions[0], dimensions[1]
        self.initialize_grid(blocks)
        self.assign_start_squares(blocks)
        for square in self.row_start_squares:
            print(square)
        print()
        for square in self.col_start_squares:
            print(square)
    
    def initialize_grid(self, blocks):
        self.grid = [[Square(row, col) for col in range(self.c)] for row in range(self.r)]
        for block in blocks:
            self.grid[block.row][block.col].is_block = True
    
    def assign_start_squares(self, blocks):
        self.row_start_squares = []
        self.col_start_squares = []
        for block in blocks:
            print(block)
            # row_start_squares
            if block.col < self.c - 1 and not [bl for bl in blocks if bl == Square(block.row, block.col + 1)]:
                length = 1
                while block.col + length < self.c - 1 and not [bl for bl in blocks if bl == Square(block.row, block.col + length)]: # not over edge of board and not over another block
                    length += 1
                self.row_start_squares.append(StartSquare(block.row, block.col + 1, length))
                print('row: ', self.row_start_squares)
            
            # col_start_squares
            if block.row < self.r - 1 and not [bl for bl in blocks if bl == Square(block.row + 1, block.col)]:
                length = 1
                while block.row + length < self.r - 1 and not [bl for bl in blocks if bl == Square(block.row + length, block.col)]: # not over edge of board and not over another block
                    length += 1
                self.col_start_squares.append(StartSquare(block.row + 1, block.col, length))
                print('col: ', self.col_start_squares)