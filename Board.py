from Square import *
import random

class Board:
    # ATTRIBUTES
    # r, c: number of rows and columns, respectively
    # grid: dictionary from Squares to their characters
    # row_start_squares: list of row start squares, ordered by row then column (increasing)
    # col_start_squares: list of col start squares
    # square_to_row_start: dictionary of squares to their row_starts
    # square_to_col_start: dictionary of squares to their col_starts
    # incomplete_row_start_squares: row StartSquares to fill
    # inserted_words: list of words that have been inserted
    # word_bank: words that can be used to fill the board

    # METHODS
    # generate_boards(words): generates all boards with desired words
    # generate_filled: generates board filled with 'valid' words

    # HELPERS
    # print_starts(): prints board with >, v, and X indicating row, column, and both starts respectively

    def __init__(self, dimensions, word_bank, blocks=[], specified_chars={}):
        self.r, self.c = dimensions[0], dimensions[1]
        self.square_to_row_start, self.square_to_col_start = {}, {}
        self.row_start_squares, self.col_start_squares = self.assign_start_squares(blocks) # also assigns square_to_row_ and col_start
        self.incomplete_row_start_squares = list(self.row_start_squares)
        self.grid = self.initialize_grid(blocks, specified_chars)
        self.word_bank = word_bank

        self.inserted_words = []
    
    def initialize_grid(self, blocks, specified_chars):
        grid = {}
        for row in range(self.r):
            for col in range(self.c):
                square = Square(row, col)
                this_char = specified_chars.get(Square(row, col), '_')
                grid[square] = this_char
                if this_char != '_': # if character given
                    col_start = self.square_to_col_start[square]
                    col_start.word[square.row - col_start.row] = this_char

                    row_start = self.square_to_col_start[square]
                    row_start.word[square.col - row_start.col] = this_char
                    
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
                while length < self.c - 1 and not Square(row, length + 1) in blocks: # not over edge of board and not over another block
                    length += 1
                    squares.append(Square(row, length))
                row_start = StartSquare(row, 0, length + 1)
                row_start_squares.append(row_start)
                for square in squares: # assign collected squares
                    self.square_to_row_start[square] = row_start
                
        
        # add ColumnStartSquares for edges of board
        for col in range(self.c):
            if not Square(0, col) in blocks:
                length = 0
                squares = [Square(length, col)]
                while length < self.r - 1 and not Square(length + 1, col) in blocks: # not over edge of board and not over another block
                    length += 1
                    squares.append(Square(length, col))

                col_start = StartSquare(0, col, length + 1)
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
                col_start = StartSquare(block.row + 1, block.col, length)
                col_start_squares.append(col_start)
                for square in squares:
                    self.square_to_col_start[square] = col_start

        return row_start_squares, col_start_squares
    
    def generate_needed_words(self, needed_words):
        # add needed_words to word_bank
        for word in needed_words:
            self.word_bank.insert(word)
        sorted_words = sorted(needed_words, key=len, reverse=True)
        yield from self.generate_needed_words_helper(sorted_words)
    
    def generate_needed_words_helper(self, needed_words, rows_only=False, cols_only=False): # rows_ and cols_only for testing
        if len(needed_words) == 0:
            yield self
            return
        
        word = needed_words[0]
        length = len(word)

        if not cols_only:
            viable_row_starts = [square for square in self.incomplete_row_start_squares if square.len == length]
            for row_start in viable_row_starts:
                changed_words = self.insert_word_at_start_square(word, row_start, row=True) # insert word
                if type(changed_words) == dict: # if successful
                    yield from self.generate_needed_words_helper(needed_words[1:]) # recurse
                    self.undo_insertion(changed_words, row=True) # undo inserting word
        
        if not rows_only:
            viable_col_starts = [square for square in self.col_start_squares if square.len == length]
            # do same with col_starts
            for col_start in viable_col_starts:
                changed_words = self.insert_word_at_start_square(word, col_start, col=True)
                if type(changed_words) == dict:
                    yield from self.generate_needed_words_helper(needed_words[1:])
                    self.undo_insertion(changed_words, col=True)

    # returns False if cannot insert, modifies grid and returns list of Squares that were modified if it can
    # still need to do perpendicular checking
    def insert_word_at_start_square(self, word, start_square, col=False, row=False):
        if not col and not row:
            raise ValueError("Must specify row or col")
        # print('trying to insert', word, 'at', start_square)

        if col:
            return_val = self.insert_word_at_col_start(word, start_square)
        else:
            return_val = self.insert_word_at_row_start(word, start_square)
        if type(return_val) == dict: # if word has been inserted
            self.inserted_words.append(word)
            # print('successful!')
            # self.print_starts()
        return return_val

    def insert_word_at_row_start(self, word, row_start):
        row, col = row_start.row, row_start.col
        changed_squares = {} # square to word index, to return

        # go through squares, checking for validity
        for i in range(len(word)):
            square = Square(row, col + i)
            if self.grid[square] != '_': # if established with letter already
                if self.grid[square] != word[i]: # if wrong letter. otherwise look at next square
                    return False
            else:
                # perpendicular testing
                if not self.is_perpendicular_valid(square, word[i], col=True):
                    return False
                changed_squares[square] = i
        
        # if valid, insert (should maybe replace with looped insert_char call?)
        self.incomplete_row_start_squares.remove(row_start)
        for square in changed_squares:
            letter = word[changed_squares[square]]

            self.grid[square] = letter # change grid
            col_start = self.square_to_col_start[square]
            col_start.word[square.row - col_start.row] = letter # change col_start's word
        
        row_start.word = list(word)
        return changed_squares
    
    def insert_word_at_col_start(self, word, col_start):
        row, col = col_start.row, col_start.col
        changed_squares = {} # square to word index, to return

        # go through squares, checking for validity
        for i in range(len(word)):
            square = Square(row + i, col)
            if self.grid[square] != '_': # if established with letter already
                if self.grid[square] != word[i]: # if wrong letter. otherwise look at next square
                    return False
            else:
                # perpendicular testing
                if not self.is_perpendicular_valid(square, word[i], col=False):
                    return False
                changed_squares[square] = i
        
        # if valid, insert (should maybe replace with looped insert_char call?)
        col_start.word = list(word)
        for square in changed_squares:
            letter = word[changed_squares[square]]
            self.grid[square] = letter # change grid
        
            row_start = self.square_to_row_start[square]
            row_start.word[square.col - row_start.col] = letter # change row_start's word
        return changed_squares
    
    def is_perpendicular_valid(self, square, letter, col=True): # checking column by default
        if col:
            start_square = self.square_to_col_start[square]
            changed_word = list(start_square.word)
            changed_word[square.row - start_square.row] = letter
        else:
            start_square = self.square_to_row_start[square]
            changed_word = list(start_square.word)
            changed_word[square.col - start_square.col] = letter

        template = ''.join(changed_word)
        return_list = self.word_bank.wildcard_search(template, ignore=self.inserted_words)
        random.shuffle(return_list)
        return return_list

    
    def undo_insertion(self, changed_squares, word, col=False, row=False):
        if not col and not row:
            raise ValueError("Must specify row or col")
        
        if col:
            self.undo_col_insertion(changed_squares)
        else:
            self.undo_row_insertion(changed_squares)
        self.inserted_words.remove(word)

    def undo_row_insertion(self, changed_squares):
        for square in changed_squares:
            self.grid[square] = '_' # change grid
            # revert col_starts
            col_start = self.square_to_col_start[square]
            col_start.word[square.row - col_start.row] = '_' # change col_start's word
            # revert row_starts
            row_start = self.square_to_row_start[square]
            row_start.word[square.col - row_start.col] = '_' # change row_start's word
        if changed_squares: # if word wasn't already filled, basically
            row_start = self.square_to_row_start[square]
            self.incomplete_row_start_squares.append(row_start)
    
    def undo_col_insertion(self, changed_squares):
        for square in changed_squares:
            self.grid[square] = '_' # change grid
            # revert row_starts
            row_start = self.square_to_row_start[square]
            row_start.word[square.col - row_start.col] = '_' # change row_start's word
            # revert col_starts
            col_start = self.square_to_col_start[square]
            col_start.word[square.row - col_start.row] = '_' # change col_start's word
    
    def generate_filled(self):
        self.incomplete_row_start_squares.sort(key=lambda x: x.col)
        self.incomplete_row_start_squares.sort(key=lambda x: x.row)
        yield from self.generate_filled_helper()
    
    def generate_filled_helper(self):
        self.print_starts()
        print(self.row_start_squares)
        print(self.col_start_squares)
        print()
        if self.incomplete_row_start_squares == []:
            yield self
        else:
            row_start = self.incomplete_row_start_squares[0]
            pattern = ''.join(row_start.word)
            #print('row_start:', row_start)
            #print('pattern:', pattern)
            potential_words = self.word_bank.wildcard_search(pattern, ignore=self.inserted_words)
            random.shuffle(potential_words)
            # print('potential words:', potential_words)

            # print()
            for word in potential_words:
                undo_input = self.insert_word_at_start_square(word, row_start, row=True)
                if type(undo_input) == dict:
                    yield from self.generate_filled()
                    self.undo_insertion(undo_input, word, row=True)

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
        return_str = return_str.rstrip('\n')
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

def adrienne_test():
    blocks = [Square(0, 0), Square(0, 5), Square(5, 0), Square(5, 5), Square(3, 2), Square(3, 3)]                     
    specified_chars = {Square(0, 1): 'r', Square(0, 4): 'b', Square(2, 0): 'a', Square(2, 5): 'f', Square(4, 0): 't', Square(4, 5): 'y'}
    b = Board([6, 6], blocks, specified_chars)
    b.print_starts()
    g = b.generate_boards(['roob'])
    b2 = next(g)
    b2.print_starts()


    b3 = next(g)
    b3.print_starts()

if __name__ == "__main__":
    adrienne_test()