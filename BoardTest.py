import unittest
from Board import Board
from Square import *

class TestBoardGenerator(unittest.TestCase):
    def test_row_starts(self):
        b = create_board()
        row_starts = set(b.row_start_squares)
        self.assertTrue(row_starts == set([Square(0, 2), Square(1, 1), Square(2, 1), Square(2, 3),
                                          Square(3, 1), Square(3, 5), Square(4, 0), Square(4, 3),
                                          Square(5, 0), Square(5, 2)]), "row_start_square positions not as expected")
        
        # expected lengths
        lengths_to_squares = {1: [Square(2, 1), Square(3, 5), Square(5, 0)],
                              2: [Square(3, 1), Square(4, 0)],
                              3: [Square(0, 2), Square(1, 1), Square(2, 3), Square(4, 3), Square(5, 2)]}
        for length in lengths_to_squares:
            starts_list = lengths_to_squares[length]
            for square in starts_list:
                b_start = [start for start in row_starts if start == square][0]
                self.assertTrue(b_start.len == length, f'wrong row_start_square length: {b_start, b_start.len}')
    
    def test_col_starts(self):
        b = create_board()
        col_starts = set(b.col_start_squares)
        self.assertTrue(col_starts == set([Square(0, 2), Square(0, 3), Square(0, 4),
                                           Square(1, 1),
                                           Square(2, 4), Square(2, 5),
                                          Square(3, 2),
                                          Square(4, 0), Square(4, 3), Square(4, 4),
                                          Square(5, 2)]), "col_start_square positions not as expected")
        
        # expected lengths
        lengths_to_squares = {1: [Square(3, 2), Square(0, 4), Square(0, 4)],
                              2: [Square(0, 2), Square(4, 0), Square(4, 3), Square(4, 4)],
                              3: [Square(0, 3), Square(2, 5)],
                              4: [Square(1, 1)]}
        for length in lengths_to_squares:
            starts_list = lengths_to_squares[length]
            for square in starts_list:
                b_start = [start for start in col_starts if start == square][0]
                self.assertTrue(b_start.len == length, f'wrong row_start_square length: {b_start, b_start.len}')
        
        # expected words
        starts_with_chars = {Square(1, 1): ['r', '_', '_', '_'], Square(0, 2): ['_', 'o'], Square(0, 3): ['_', 'w', '_'], Square(2, 5): ['c', 'o', 'l']}
        for square in col_starts:
            if square in starts_with_chars:
                self.assertTrue(square.word == starts_with_chars[square], 'unexpected word')
            else:
                self.assertTrue(square.word == ['_'] * square.len)
    
    def test_insertion_and_undo(self):
        b = create_board()
        # insertion
        undo_input = b.insert_word_at_row_start('hoc', Square(2, 3))
        check_squares = {Square(1, 1): ['r', '_', '_', '_'], Square(0, 2): ['_', 'o'], Square(0, 3): ['_', 'w', 'h'], Square(2, 4): ['o'], Square(2, 5): ['c', 'o', 'l']}
        for square in b.col_start_squares:
            if square in check_squares:
                self.assertTrue(square.word == check_squares[square], 'unexpected word')
            else:
                self.assertTrue(square.word == ['_'] * square.len, f'unexpected length: {square}')
        
        # undoing
        b.undo_row_insertion(undo_input)
        b2 = create_board()
        self.assertTrue(b.row_start_squares == b2.row_start_squares)
        for b_col_start in b.col_start_squares:
            b2_col_start = [s for s in b2.col_start_squares if s == b_col_start][0]
            self.assertTrue(b_col_start.word == b2_col_start.word)
        
        for row in range(b.r):
            for col in range(b.c):
                s = Square(row, col)
                self.assertTrue(b.grid[s] == b2.grid[s])
    
    def test_invalid_insertion(self):
        b = create_board()
        b2 = create_board()
        b.insert_word_at_row_start('add', Square(2, 3))
        self.assertTrue(b.grid == b2.grid)
        for b_col_start in b.col_start_squares:
            b2_col_start = [s for s in b2.col_start_squares if s == b_col_start][0]
            self.assertTrue(b_col_start.word == b2_col_start.word)
    
    def test_generate_boards(self):
        # rows
        b = create_board()
        row_words = ['abc', 'row', 'm', 'efc', 'ij', 'o', 'gh', 'kll', 'd', 'nop']
        g = b.generate_boards_helper(sorted(row_words, key=len, reverse=True), rows_only=True)
        b2 = next(g)
        b2.print_starts()

        # cols
        c = create_board()
        col_words = ['ao', 'bwe', 'c', 'rdgj', 'f', 'col', 'h', 'im', 'ko', 'lp', 'n']
        g = c.generate_boards_helper(sorted(col_words, key=len, reverse=True), cols_only=True)
        c2 = next(g)
        c2.print_starts()
        self.assertTrue(c2.grid == b2.grid, "col and row grids don't match")

        # both
        d = create_board()
        g = d.generate_boards(row_words + col_words)
        d2 = next(g)
        d2.print_starts()


def create_board():
    blocks = [Square(0, 0), Square(0, 1), Square(0, 5),
                Square(1, 0), Square(1, 4), Square(1, 5),
                Square(2, 0), Square(2, 2),
                Square(3, 0), Square(3, 3), Square(3, 4),
                Square(4, 2),
                Square(5, 1), Square(5, 5)]                     
    specified_chars = {Square(1, 1): 'r', Square(1, 2): 'o', Square(1, 3): 'w',
                        Square(2, 5): 'c', Square(3, 5): 'o', Square(4, 5): 'l'}
    b = Board([6, 6], blocks, specified_chars)
    return b

if __name__ == '__main__':
    unittest.main()