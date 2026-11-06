import copy
from exceptions import *
from parser import EquationParser

class GaussianSolver():
    def __init__(self, matrix, variables=""):
        self.matrix, self.variables = copy.deepcopy(matrix), variables
        self.rows, self.columns = len(self.matrix), len(self.matrix[0])
        self.num_variables = len(self.variables)
        self.__ABSOLUTE = 1e-9

        self._check_matrix()
        self.solution = {}

    def solve(self) -> dict[str, float]:
        # Callculate the RREF of the matrix
        self._rref()
        # Check if the system is solvable
        self._check_matrix()
        
        self._find_solution()

        return self.solution


    def get_metadata(self) -> dict:
        return {"num_variables": self.num_variables, "num_equations":self.rows}

    def _rref(self):
        """Transform the matrix into Reduced Row Echelon Form (RREF)."""
        # Iterate through each column
        current_row = 0
        for current_col in range(self.columns-1):
            # print("_"*20)
            # Get first row with non-zero element in the column
            pivot_row = None
            for row in range(current_row, self.rows):
                if abs(self.matrix[row][current_col]) > self.__ABSOLUTE:
                    pivot_row = row
                    break
            # If zero column, skip it
            if pivot_row == None:
                # print("Whole column is zeros, skipped")
                continue
            # Swap the current row with the pivot_row 
            if pivot_row != current_row:
                self.matrix[pivot_row], self.matrix[current_row] = self.matrix[current_row], self.matrix[pivot_row]
            # Update the pivot 
            pivot_row = current_row
            # print(f"{current_row} swapped with {pivot_row}\n{self}")
            
            # Normalize the row
            pivot = self.matrix[current_row][current_col]
            for col in range(self.columns):
                self.matrix[current_row][col] = self._zeroize(self.matrix[current_row][col]/pivot)
            # print(f"Normalized with {pivot}\n", self)

            # Eliminate numbers above and below
            for row in range(self.rows):
                # Don't subtract the row from itself
                coeff = self.matrix[row][current_col]
                if row == current_row or coeff == 0:
                    continue
                for col in range(self.columns):
                    # print(self.matrix[row][col], self.matrix[pivot_row][col], coeff)
                    self.matrix[row][col] = self._zeroize(self.matrix[row][col]-self.matrix[pivot_row][col] * coeff)
            # print(f"Eliminated column\n{self}")
            current_row += 1

    def _check_matrix(self):
        if self.rows < len(self.variables):
            raise DimensionMismatchException(f"{self.rows} equations for {self.num_variables} variables ({self.variables})")

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

            self.solution[self.variables[j]] = self.matrix[i][-1] 


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

# matrix = [
# [1.0, 1.0, 1.0, 6.0],
# [4, 10, -2, 54],
# [2.0, 5.0, -1.0, 27.0],
# [0.0, 2.0, 5.0, -4.0],
# ]
# matrix = [
#     [0, 2, -1, -4],
#     [2, 0, -1, -11],
#     [-2, 0, 0, 22]
# # ]
# matrix = [
#     [1, 2, -1, -4],
#     [2, 3, -1, -11],
#     [-2, 0, -3, 22]
# ]

# 10x1 + 5x2 = 5
# -4x2 + 3x3 = 10
# x1 + 6x3 = 12
# x2 - 1.3*x3 = -2

# matrix = [
#     [10, 5, 0, 5],
#     [0, 4, 3, 10],
#     [1, 0, 6, 12],
# ]


# parser = EquationParser("pyeqsolver\\equations.txt")
# equations, vars = parser.parse()
# print(equations)
# g = GaussianSolver(equations, vars)
# print(g)
# g.solve()
# print(g)
# print(g.solution)

