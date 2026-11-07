import json
from solver import *

class JSONExporter():
    def __init__(self, output_path):
        self.output_path = output_path

    def save(self, solutions, metadata):
        result = {"status":"SUCCESS",
                  "system_info":metadata,
                  "solution":solutions}
        with open(self.output_path, 'w') as f:
            json.dump(result, f, indent=2)


parser = EquationParser("pyeqsolver/equations.txt")

equations, vars = parser.parse()
solver = GaussianSolver(matrix=equations, variables=vars)
solutions = solver.solve()
print(solutions)

exporter = JSONExporter(output_path="data/solution.json")
exporter.save(solutions=solutions, metadata=solver.get_metadata())