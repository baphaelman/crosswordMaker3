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