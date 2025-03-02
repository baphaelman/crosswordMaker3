from Square import *

class Board:
    # ATTRIBUTES
    # r, c: number of rows and columns, respectively
    # grid: rxc matrix of Squares
    # row_start_squares: list of row start squares, ordered by row then column (increasing)
    # col_start_squares: list of col start squares

    def __init__(self, dimensions, blocks):
        self.r, self.c = dimensions[0], dimensions[1]
        self.grid = self.initialize_grid(blocks)
        self.row_start_squares, self.col_start_squares = self.assign_start_squares(blocks)
    
    def initialize_grid(self, blocks):
        grid = [["_" for col in range(self.c)] for row in range(self.r)]
        for block in blocks:
            grid[block.row][block.col] = "#"
        return grid
    
    def assign_start_squares(self, blocks):
        row_start_squares = []
        col_start_squares = []
        for block in blocks:
            # row_start_squares
            row_square = Square(block.row, block.col + 1)
            if block.col < self.c - 1 and not row_square in blocks:
                length = 1
                while block.col + length < self.c - 1 and not row_square in blocks: # not over edge of board and not over another block
                    length += 1
                row_start_squares.append(StartSquare(block.row, block.col + 1, length))
            
            # col_start_squares
            col_square = Square(block.row + 1, block.col)
            if block.row < self.r - 1 and not col_square in blocks:
                length = 1
                while block.row + length < self.r - 1 and not col_square in blocks: # not over edge of board and not over another block
                    length += 1
                col_start_squares.append(ColumnStartSquare(block.row + 1, block.col, length))

        # add StartSquares for edges of board
        for row in range(self.r):
            edge_row_square = Square(row, 0)
            if not edge_row_square in blocks:
                length = 1
                while block.col + length < self.c - 1 and not edge_row_square in blocks: # not over edge of board and not over another block
                    length += 1
                row_start_squares.append(StartSquare(row, 0, length))
        
        # add ColumnStartSquares for edges of board
        for col in range(self.c):
            edge_col_square = Square(0, col)
            if not edge_col_square in blocks:
                length = 1
                while block.row + length < self.r - 1 and not edge_col_square in blocks: # not over edge of board and not over another block
                    length += 1
                col_start_squares.append(ColumnStartSquare(0, col, length))

        return row_start_squares, col_start_squares

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
                this_square = Square(row, col)
                if this_square in self.row_start_squares:
                    if this_square in self.col_start_squares:
                        return_str += "X "
                    else:
                        return_str += "> "
                elif this_square in self.col_start_squares:
                    return_str += "v "
                else:
                    return_str += self.grid[row][col] + " "
            return_str += "\n"
        print(return_str)