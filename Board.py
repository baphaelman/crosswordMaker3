from Square import *

class Board:
    # ATTRIBUTES
    # r, c: number of rows and columns, respectively
    # grid: dictionary from Squares to their characters
    # row_start_squares: list of row start squares, ordered by row then column (increasing)
    # col_start_squares: list of col start squares
    # square_to_row_start: dictionary of squares to their row_starts
    # square_to_col_start: dictionary of squares to their col_starts

    # METHODS
    # generate_boards(words): generates all boards with desired words

    # HELPERS
    # print_starts(): prints board with >, v, and X indicating row, column, and both starts respectively

    def __init__(self, dimensions, blocks, specified_chars):
        self.r, self.c = dimensions[0], dimensions[1]
        self.square_to_row_start, self.square_to_col_start = {}, {}
        self.row_start_squares, self.col_start_squares = self.assign_start_squares(blocks) # also assigns square_to_row_ and col_start
        self.grid = self.initialize_grid(blocks, specified_chars)
    
    def initialize_grid(self, blocks, specified_chars):
        grid = {}
        for row in range(self.r):
            for col in range(self.c):
                square = Square(row, col)
                this_char = specified_chars.get(Square(row, col), '_')
                grid[square] = this_char
                if this_char != '_': # if character given
                    start_square = self.square_to_col_start[square]
                    start_square.word[square.row - start_square.row] = this_char
                    
        for block in blocks:
            grid[block] = "#"
        return grid
    
    def assign_start_squares(self, blocks):
        row_start_squares = []
        col_start_squares = []

        # add StartSquares for edges of board
        for row in range(self.r):
            if not Square(row, 0) in blocks:
                length = 0
                squares = [Square(row, length)]
                while length < self.c - 1 and not Square(row, length) in blocks: # not over edge of board and not over another block
                    length += 1
                    squares.append(Square(row, length))
                row_start = StartSquare(row, 0, length)
                row_start_squares.append(row_start)
                for square in squares: # assign collected squares
                    self.square_to_row_start[square] = row_start
                
        
        # add ColumnStartSquares for edges of board
        for col in range(self.c):
            if not Square(0, col) in blocks:
                length = 0
                squares = [Square(length, col)]
                while length < self.r - 1 and not Square(length, col) in blocks: # not over edge of board and not over another block
                    length += 1
                    squares.append(Square(length, col))
                col_start = ColumnStartSquare(0, col, length)
                col_start_squares.append(col_start)
                for square in squares: # assign collected squares
                    self.square_to_col_start[square] = col_start

        # add StartSquares (and squares_to_starts values) in relation to blocks
        for block in blocks:
            # row_start_squares
            row_square = Square(block.row, block.col + 1)
            if block.col < self.c - 1 and not row_square in blocks:
                length = 1
                squares = [row_square]
                while block.col + length < self.c - 1 and not Square(block.row, block.col + length + 1) in blocks: # not over edge of board and not over another block
                    length += 1
                    squares.append(Square(block.row, block.col + length))
                row_start = StartSquare(block.row, block.col + 1, length)
                row_start_squares.append(row_start)
                for square in squares:
                    self.square_to_row_start[square] = row_start
            
            # col_start_squares
            col_square = Square(block.row + 1, block.col)
            if block.row < self.r - 1 and not col_square in blocks:
                length = 1
                squares = [col_square]
                while block.row + length < self.r - 1 and not Square(block.row + length + 1, block.col) in blocks: # not over edge of board and not over another block
                    length += 1
                    squares.append(Square(block.row + length, block.col))
                col_start = ColumnStartSquare(block.row + 1, block.col, length)
                col_start_squares.append(col_start)
                for square in squares:
                    self.square_to_col_start[square] = col_start

        return row_start_squares, col_start_squares
    
    def generate_boards(self, needed_words):
        sorted_words = sorted(needed_words, reverse=True)
        yield from self.generate_boards_helper(sorted_words)
    
    def generate_boards_helper(self, needed_words):
        if len(needed_words) == 0:
            return
        
        word = needed_words[0]
        length = len(word)
        viable_row_starts = [square for square in self.row_start_squares if square.len == length]
        viable_col_starts = [square for square in self.col_start_squares if square.len == length]

        for row_start in viable_row_starts:
            return False
            # insert word
            # yield from self.generate_boards_helper(needed_words[1:])
            # undo inserting word
                

    # returns False if cannot insert, modifies grid and returns list of Squares that were modified if it can
    #def insert_word_at_row_start(self, word, row_start):


    def __repr__(self):
        return_str = ""
        for row in range(self.r):
            for col in range(self.c):
                square = Square(row, col)
                return_str += self.grid[square] + " "
            return_str += "\n"
        return return_str
    
    def print_starts(self):
        return_str = ""
        for row in range(self.r):
            for col in range(self.c):
                square = Square(row, col)
                if self.grid[square] != "_": # if character at square
                    return_str += self.grid[square] + " "
                else:
                    if square in self.row_start_squares:
                        if square in self.col_start_squares: # if both column and row start
                            return_str += "X "
                        else: # if just row start
                            return_str += "> "
                    elif square in self.col_start_squares: # if just column start
                        return_str += "v "
                    else:
                        return_str += self.grid[square] + " " # if empty and 'center'
            return_str += "\n"
        print(return_str)

def square_to_starts_test():
    specified_chars = {Square(4, 5): 'r', Square(4, 6): 'o', Square(4, 7): 'w'}                                                
    blocks = [Square(0, 6), Square(0, 7), Square(1, 7), Square(3, 2), Square(3, 3), Square(4, 4), Square(5, 5), Square(5, 6), Square(5, 0), Square(6, 0), Square(6, 1), Square(7, 0), Square(7, 1), Square(7, 2), Square(7, 3)]
    b = Board([8, 8], blocks, specified_chars)

    for row in range(b.r):
        for col in range(b.c):
            s = Square(row, col)
            if not b.grid[s] == "#":
                string = str(b.square_to_row_start[Square(row, col)])
                string += " " + str(b.square_to_col_start[Square(row, col)])
                print(string)
        print()

if __name__ == "__main__":
    square_to_starts_test()