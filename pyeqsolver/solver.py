import copy
from .exceptions import *

class GaussianSolver():
    def __init__(self, matrix, variables=""):
        self.matrix, self.variables = copy.deepcopy(matrix), variables
        self.rows, self.columns = len(self.matrix), len(self.matrix[0])
        self.num_variables = len(self.variables)
        self.__ABSOLUTE = 1e-9

        self._check_matrix()
        self.solutions = {}

    def solve(self) -> dict[str, float]:
        # Callculate the RREF of the matrix
        self._rref()
        # Check if the system is solvable
        self._check_matrix()
        
        self._find_solution()

        return self.solutions


    def get_metadata(self) -> dict:
        return {"num_variables": self.num_variables, "num_equations":self.rows}

    def _rref(self):
        """Transform the matrix into Reduced Row Echelon Form (RREF)."""
        # Iterate through each column
        current_row = 0
        for current_col in range(self.columns-1):
            # Get maximum absolute pivot in the column (at first assume maximum pivot is the curront one)
            max_pivot = self.matrix[current_row][current_col]
            max_pivot_idx = current_row
            for row in range(current_row, self.rows):
                if abs(self.matrix[row][current_col] )> abs(max_pivot):
                    max_pivot = self.matrix[row][current_col]
                    max_pivot_idx = row

            # If zero column, skip it
            if max_pivot == 0: 
                continue
            pivot_row = max_pivot_idx

            # Swap rows (if found larger pivot)
            if pivot_row != current_row:
                self.matrix[pivot_row], self.matrix[current_row] = self.matrix[current_row], self.matrix[pivot_row]
            # Update the pivot 

            # Normalize the row
            pivot = self.matrix[current_row][current_col]
            for col in range(self.columns):
                self.matrix[current_row][col] = self._zeroize(self.matrix[current_row][col]/pivot)

            # Eliminate numbers above and below
            for row in range(self.rows):
                # Don't subtract the row from itself
                coeff = self.matrix[row][current_col]
                if row == current_row or coeff == 0:
                    continue
                for col in range(self.columns):
                    self.matrix[row][col] = self._zeroize(self.matrix[row][col]-self.matrix[current_row][col] * coeff)
            current_row += 1

    def _check_matrix(self):
        if self.rows < len(self.variables):
            # Create the message
            msg = ''
            for i, var in enumerate(self.variables):
                msg += var
                if i < self.num_variables-1:
                    msg += ", "
            raise DimensionMismatchException(f"{self.rows} equations for {self.num_variables} variables ({msg})")

        num_zero_rows = 0
        for i in range(self.rows):
            # If the row is not 0s, skip it
            if not self._is_zero_row(self.matrix[i][:-1]):
                    continue
            # A row whose coefficients are all zero but whose constant is not
            if self.matrix[i][-1] != 0:
                raise InconsistentSystemException(f"The system has no solution (row reduces to 0 = {self.matrix[i][-1]})")
            # A row and its constant are zero 
            else:
                num_zero_rows += 1
        rank = self.rows - num_zero_rows
        if  rank < self.num_variables:
            raise InfiniteSolutionsException(f"Infinitely many solutions: rank {rank} < {self.num_variables} variables")


    def _find_solution(self):
        for i in range(self.rows):
            # If zero row, skip it
            if self._is_zero_row(self.matrix[i][:-1]):
                continue

            j = 0
            while j < self.columns and self.matrix[i][j] == 0:
                j += 1

            self.solutions[self.variables[j]] = self.matrix[i][-1] 


    def _is_zero_row(self, row):
        for j in range(len(row)):
            if row[j] != 0:
                return False
        return True

            
    def _zeroize(self, num):
        return num if abs(num) > self.__ABSOLUTE else 0



    def __str__(self):
        result = "Equations matrix:\n["
        for row in self.matrix:
            result += str(row) + ",\n"
        result = result[:-1] + "]"
        return result