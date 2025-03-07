class Square:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    def __repr__(self):
        return "(" + str(self.row) + "," + str(self.col) + ")"
    
    def __eq__(self, other):
        if not isinstance(other, Square):
            return NotImplemented
        return self.row == other.row and self.col == other.col
    
    def __hash__(self):
        return hash((self.row, self.col))

""""
class StartSquare(Square):
    def __init__(self, row, col, len):
        self.row = row
        self.col = col
        self.len = len
    
    def __repr__(self):
        return "(" + str(self.row) + "," + str(self.col) + "," + str(self.len) + ")"
"""

class StartSquare(Square):
    def __init__(self, row, col, len):
        super().__init__(row, col)
        self.len = len
        self.word = ["_" for _ in range(self.len)]
    
    def __repr__(self):
        return "(" + str(self.row) + "," + str(self.col) + "," + str(self.word) + ")" # fix str(self.word) lol