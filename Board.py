from Square import *

class Board:
    # ATTRIBUTES
    # r, c: number of rows and columns, respectively
    # grid: rxc matrix of Squares
    # row_start_squares: list of row start squares, ordered by row then column (increasing)
    # col_start_squares: list of col start squares

    # METHODS
    # generate_boards(words): generates all boards with desired words

    # HELPERS
    # print_starts(): prints board with >, v, and X indicating row, column, and both starts respectively

    def __init__(self, dimensions, blocks, specified_chars):
        self.r, self.c = dimensions[0], dimensions[1]
        self.grid = self.initialize_grid(blocks, specified_chars)
        self.row_start_squares, self.col_start_squares = self.assign_start_squares(blocks)
    
    def initialize_grid(self, blocks, specified_chars):
        grid = [["" for col in range(self.c)] for row in range(self.r)]
        for row in range(self.r):
            for col in range(self.c):
                square = Square(row, col)
                if square in specified_chars:
                    grid[row][col] = specified_chars[square]
                else:
                    grid[row][col] = "_"

        for block in blocks:
            grid[block.row][block.col] = "#"
        return grid
    
    def assign_start_squares(self, blocks):
        row_start_squares = []
        col_start_squares = []

        # add StartSquares for edges of board
        for row in range(self.r):
            edge_row_square = Square(row, 0)
            if not edge_row_square in blocks:
                length = 1
                while length < self.c - 1 and not Square(row, length) in blocks: # not over edge of board and not over another block
                    length += 1
                row_start_squares.append(StartSquare(row, 0, length))
        
        # add ColumnStartSquares for edges of board
        for col in range(self.c):
            edge_col_square = Square(0, col)
            if not edge_col_square in blocks:
                length = 1
                while length < self.r - 1 and not Square(length, col) in blocks: # not over edge of board and not over another block
                    length += 1
                col_start_squares.append(ColumnStartSquare(0, col, length))

        # add StartSquares in relation to blocks
        for block in blocks:
            # row_start_squares
            row_square = Square(block.row, block.col + 1)
            if block.col < self.c - 1 and not row_square in blocks:
                length = 1
                while block.col + length < self.c - 1 and not Square(block.row, block.col + length + 1) in blocks: # not over edge of board and not over another block
                    length += 1
                row_start_squares.append(StartSquare(block.row, block.col + 1, length))
            
            # col_start_squares
            col_square = Square(block.row + 1, block.col)
            if block.row < self.r - 1 and not col_square in blocks:
                length = 1
                while block.row + length < self.r - 1 and not Square(block.row + length + 1, block.col) in blocks: # not over edge of board and not over another block
                    length += 1
                col_start_squares.append(ColumnStartSquare(block.row + 1, block.col, length))

        return row_start_squares, col_start_squares
    
    def generate_boards(self, needed_words):
        sorted_words = sorted(needed_words, reverse=True)
        yield from self.generate_boards_helper(sorted_words)
    
    def generate_boards_helper(self, needed_words):
        if len(needed_words) == 0:
            yield
        
        word = needed_words[0]
        length = len(word)
        viable_row_starts = [square for square in self.row_start_squares if square.len == length]
        viable_col_starts = [square for square in self.col_start_squares if square.len == length]

        for row_start in viable_row_starts:
            if self.insert_word_at_row_start(word, row_start):
                return False

    # returns False if cannot insert, modifies grid and returns list of Squares that were modified if it can
    #def insert_word_at_row_start(self, word, row_start):


    def __repr__(self):
        return_str = ""
        for row in range(self.r):
            for col in range(self.c):
                return_str += self.grid[row][col] + " "
            return_str += "\n"
        return return_str
    
    def print_starts(self):
        return_str = ""
        for row in range(self.r):
            for col in range(self.c):
                if self.grid[row][col] != "_": # if character at square
                    return_str += self.grid[row][col] + " "
                else:
                    this_square = Square(row, col)
                    if this_square in self.row_start_squares:
                        if this_square in self.col_start_squares: # if both column and row start
                            return_str += "X "
                        else: # if just row start
                            return_str += "> "
                    elif this_square in self.col_start_squares: # if just column start
                        return_str += "v "
                    else:
                        return_str += self.grid[row][col] + " " # if empty and 'center'
            return_str += "\n"
        print(return_str)