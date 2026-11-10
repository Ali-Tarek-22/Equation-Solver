from pyeqsolver import EquationParser, GaussianSolver, JSONExporter
from pyeqsolver.exceptions import PyEqSolverError


exporter = JSONExporter(output_path="data/solution.json")

try:
    # 1. Parse equations from the file
    parser = EquationParser(file_path="data/input_equations.txt")
    matrix, variables = parser.parse()

    # 2. Solve with Gaussian Elimination
    solver = GaussianSolver(matrix=matrix, variables=variables)
    solutions = solver.solve()   # {'x1': 0.0, 'x2': 1.0, 'x3': 2.0}

    # 3. Export the result
    exporter.save(solutions=solutions, metadata=solver.get_metadata())
    print("Solved. Results written to data/solution.json")

except (PyEqSolverError, FileNotFoundError) as e:
    exporter.save_error(e)
    print(f"Could not solve the system: {e}")