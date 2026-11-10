import unittest
# from ..pyeqsolver.solver import * # Only works if you run the script as a module from outside the folder

import sys
import os

# pyeqsolver absolute path 
target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../pyeqsolver"))

# Add it to sys.path before importing
sys.path.insert(0, target_dir)

from solver import EquationParser, GaussianSolver
from exceptions import *




class TestSolver(unittest.TestCase):
    @classmethod
    def setUpClass(cls): # Run once at the beginning
        #  return super().setUpClass()(cls):
        pass

    @classmethod
    def tearDownClass(cls): # Run once at the end
        #  return super().tearDownClass()
        pass

    def setUp(self): # Run before each test
        #  return super().setUp()
        pass
    def tearDown(self): # Run after each test
        # return super().tearDown()
        pass

    def test_solver_1(self): # Must start with test
        matrix = [
            [10, 5, 0, 5],
            [0, 4, 3, 10],
            [1, 0, 6, 12],
        ]
        vars = ['x1', 'x2', 'x3']
        g = GaussianSolver(matrix, vars)
        solutions = g.solve()

        self.assertEqual(solutions, {'x1': 0, 'x2': 1.0, 'x3': 2.0})
    def test_solver_2(self): # Must start with test
        matrix = [
            [1, 1, 1, 6],
            [0, 2, 5, -4],
            [2, 5, -1, 27],
        ]
        vars = ['x', 'y', 'z']
        g = GaussianSolver(matrix, vars)
        solutions = g.solve()

        self.assertEqual(solutions, {'x': 5.0, 'y': 3.0, 'z': -2.0})

    def test_solver_3(self): # Must start with test
        matrix = [
            [1, 1, 1, 1, 10],
            [2, 3, -1, 4, 21],
            [3, -1, 2, -1, 3],
            [4, 2, -3, 1, 3],
        ]
        vars = ['x', 'y', 'z', 'w']
        g = GaussianSolver(matrix, vars)
        solutions = g.solve()

        self.assertEqual(solutions, {'x': 1.0, 'y': 2.0, 'z': 3.0, 'w':4})

    def test_solver_4(self): # Must start with test
        matrix = [
            [3, 2, 5],
            [6, 4, 8],
        ]
        vars = ['x', 'y']
        g = GaussianSolver(matrix, vars)
        # solutions = g.solve()

        self.assertRaises(InconsistentSystemException, g.solve) # Send error type and method (then parameters if the method accepts)

    def test_solver_5(self): # Must start with test
        matrix = [
            [0.00000001, 1, 1],
            [1, 1, 2]
        ]
        vars = ['x', 'y']
        g = GaussianSolver(matrix, vars)
        solutions = g.solve()

        self.assertEqual(solutions, {'x': 1.00000001, 'y': 0.99999999})

    def test_solver_6(self): # Must start with test
        matrix = [
            [1, 1, 1, 6],
            [1, 1, 2, 9],
            [1, 2, 1, 8]
        ]
        vars = ['x', 'y', 'z']
        g = GaussianSolver(matrix, vars)
        solutions = g.solve()

        self.assertEqual(solutions, {'x': 1, 'y': 2, 'z': 3})

    def test_solver_7(self): # Must start with test
        matrix = [
            [1, 1, -1, 10],
            [0, 1, 0, 15],
            [1, -1, 1, 5]
        ]
        vars = ['x', 'y', 'z']
        g = GaussianSolver(matrix, vars)
        solutions = g.solve()

        self.assertEqual(solutions, {'x': 7.5, 'y': 15.0, 'z': 12.5})

# To be able to run the script directly:
if __name__ == "__main__":
    unittest.main()