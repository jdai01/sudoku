import pandas as pd
from collections import Counter

DOMAIN = [str(i) for i in range(1,10)]
EXCLUDE = ['0', None]
N = 9

class Sudoku:

    def __init__(self, filename=None):
        """
        Initialize Sudoku from a file.
        """
        if filename:
            with open(filename, 'r') as f:
                data = [list(row.strip()) for row in f.readlines()]
                self.board = pd.DataFrame(data)
        else:
            # Empty board
            self.board = pd.DataFrame([['0'] * N for _ in range(N)])

    @staticmethod
    def check_constraint(l: list):
        """
        Check if a row/column/block list has no duplicates excluding zeros.
        """
        c = Counter(l)
        c = Counter({k: v for k, v in c.items() if k not in EXCLUDE}) # Excludes 0 or None
        return all(v == 1 for v in c.values())

    def check_valid(self):
        """
        Check if the board satisfies Sudoku constraints so far.
        """

        # Check all rows and columns
        for i in range(N):
            # Row
            if not self.check_constraint(list(self.board.iloc[i])):
                return False
            # Column
            if not self.check_constraint(list(self.board.iloc[:, i])):
                return False
            
        # Check all 3x3 blocks
        for i in range(0, N, 3):        # Row start index
            for j in range(0, N, 3):    # Column start index
                block = self.board.iloc[i:i+3, j:j+3].values.flatten().tolist()

                if not self.check_constraint(block):
                    return False
        
        return True
    
    def find_empty(self):
        """
        Find the next empty cell (marked '0') to fill.
        Returns a tuple (row, col) or None if full.
        """
        for i in range(N):
            for j in range(N):
                if self.board.iat[i, j] == '0':
                    return i, j
        return None

    def possible_values(self, row, col):
        """
        Return a list of possible values for the cell at (row, col).
        """
        if self.board.iat[row, col] != '0':
            return []

        # Collect digits already present in row, col, and block
        row_vals = set(self.board.iloc[row])
        col_vals = set(self.board.iloc[:, col])

        # Identify top-left corner of 3x3 block
        block_row_start = (row // 3) * 3
        block_col_start = (col // 3) * 3
        block_vals = set(self.board.iloc[block_row_start:block_row_start+3, block_col_start:block_col_start+3].values.flatten())

        used = row_vals.union(col_vals).union(block_vals)
        used.discard('0')  # remove empty cell marker

        return [v for v in DOMAIN if v not in used]

    def solve(self) -> bool:
        """
        Solve the Sudoku board using backtracking.
        Returns True if solved, False if no solution.
        """
        empty = self.find_empty()
        if not empty:
            # No empty cells => solved
            return True

        row, col = empty
        for val in self.possible_values(row, col):
            self.board.iat[row, col] = val
            if self.check_valid():
                if self.solve():
                    return True
            # Backtrack
            self.board.iat[row, col] = '0'

        return False
    
    def __str__(self):
        """
        Pretty-print the board in Sudoku style.
        """
        output = ['-'*13]
        for i in range(N):
            row = [x if x not in EXCLUDE else ' ' for x in list(self.board.iloc[i])]   # Replace 0 or None with ' '
            output.append("".join("|" + "".join(row[i:i+3]) for i in range(0, N, 3)) + '|') # Join with '|'

            if (i+1) % 3 == 0:
                output.append('-'*13)

        return "\n".join(output)