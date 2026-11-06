import re
from collections import defaultdict
from exceptions import * 

class EquationParser():
    def __init__(self, file_path):
        self.file_path = file_path


    def parse(self) -> tuple[list[list[float]], list[str]]:
        # Read the file
        try:
            with open(self.file_path, 'r') as file:
                lines = file.readlines()

            vars = [] # To store variables characters
            results = [] # To temporarly store the RHS of the equations 
            equations = [] # The final matrix


            eq_num = 0 # To trach current equation
            for i, line in enumerate(lines, start=1):

                # Remove all spaces and \n  
                line = line.strip().replace(" ", "")

                # If empty line or comment skip it 
                if not len(line) or line[0] == '#':
                    continue

                # Check for invalid characters
                valid_characters = set("-+*=_.")
                for char in line:
                    if char not in valid_characters:
                        raise InvalidFileFormatException(f"Line {i}: Invalid character {char} in {line}")

                # Split RHS and LHS
                left, right = line.replace.split('=')


                # Split LHS by operators
                # left = re.split(r'(\+|\-|\*)', left)
                left = re.split(r'(\+|\-)', left)
                # Neglect empty strings
                left = [s for s in left if s]

                # Create a map of variables
                coef_var = defaultdict(float) # Var: Coeff
                # Create a new row for this equation
                equations.append([0]*len(vars)) # Add a new line for this equation
                negative = False # Negative flag
                j = 0

                # Iterate through LHS
                for segment in left:
                    # If first character in line is "-" raise a flag
                    if segment[j] in ['+', '-']:
                        negative = segment == '-'
                        j = 0
                        continue

                    # Read the coefficient of the variable
                    coeff = ''
                    while segment[j].isdigit() or segment[j] == '.':
                        coeff += segment[j]
                        j += 1
                    # Convert to float, make it 1 if no coefficient detected
                    coeff = float(coeff) if coeff else 1.0
                    # Negate the coefficient of negative flag is raised
                    coeff = -coeff if negative else coeff

                    # If there's * or skip
                    if segment[j] == "*":
                        j += 1
                    # If * then something, raise error
                    if len(segment[j:]) == 0:
                        raise InvalidFileFormatException(f"Line {i}: * with two operator after each other in {line}")
                    
                    # Save the variable as the rest of the segment
                    variable = segment[j:]

                    # Check the variable:
                    if variable[0].isnumeric():
                        raise InvalidFileFormatException(f"Line {i}: Invalid variable name {variable} in {line}")

                    
                    # If new variable, add it and increase all equation sizes
                    if variable not in vars:
                        vars.append(variable)
                        for eq in equations:
                            eq.append(0)

                    # Update the map
                    coef_var[variable] += coeff
                    j = 0

                # Add coefficient to matrix:
                for var in vars:
                    equations[eq_num][vars.index(var)] = coef_var[var]

                # Save the RHS if correct
                try:
                    results.append(float(right)) # Append the RHS value
                except ValueError:
                    raise InvalidFileFormatException(f"Line {i}: Invalid RHS {right} in {line}")
                
                eq_num += 1

            for i, eq in enumerate(equations):
                eq.append(results[i])

            return equations, vars
        except Exception:
            pass



test = EquationParser("pyeqsolver\\equations.txt")
equations, vars = test.parse()
print(equations)
print(vars)

