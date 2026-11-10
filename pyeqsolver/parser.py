import re
import string
from collections import defaultdict
from .exceptions import * 

class EquationParser():
    def __init__(self, file_path):
        self.file_path = file_path


    def parse(self) -> tuple[list[list[float]], list[str]]:
        # Read the file
        try:
            with open(self.file_path, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError: # File not found
            raise FileNotFoundError(f'The path "{self.file_path}" doesn\'t exist')

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
            valid_chars = set(string.ascii_letters + string.digits + "-+*=_.")
            valid_variables = set(string.ascii_letters + string.digits + "_")
            for char in line:
                if char not in valid_chars:
                    raise InvalidFileFormatException(f"Line {i}: Invalid character '{char}' in {line}")

            # Split RHS and LHS
            split_line = line.split('=')

            if len(split_line) != 2:
                raise InvalidFileFormatException(f"Line {i}: no or more than one '=' in {line}")
            left, right = split_line    


            # Split LHS by operators
            # left = re.split(r'(\+|\-|\*)', left)
            left = re.split(r'(\+|\-)', left)
            # Neglect empty strings
            left = [s for s in left if s]
            if len(left) == 0:
                raise InvalidFileFormatException(f"Line {i}: Empty LHS in {line}")

            coef_var = defaultdict(float) # # Create a map of variables | Var: Coeff
            equations.append([0]*len(vars)) # Add a new line for this equation
            negative = False # Negative flag
            last_operator = False # To check for consecitive operators
            j = 0

            # Iterate through LHS
            for segment in left:
                # If first character in line is "-" raise a flag
                if segment[j] in ['+', '-']:
                    if last_operator: # If two consecitive operators, raise error
                        raise InvalidFileFormatException(f"Line {i}: Can't have multiple operators in a row in {line}")
                    last_operator = True
                    negative = segment == '-'
                    j = 0
                    continue
                else:
                    last_operator = False

                # Read the coefficient of the variable
                coeff = ''
                while segment[j].isdigit() or segment[j] == '.':
                    coeff += segment[j]
                    j += 1
                    if j == len(segment):
                        raise InvalidFileFormatException(f"Line {i}: operator missing in {line}")
                    
                # Convert to float, make it 1 if no coefficient detected
                coeff = float(coeff) if coeff else 1.0
                # Negate the coefficient of negative flag is raised
                coeff = -coeff if negative else coeff

                # If there's * skip
                if segment[j] == "*":
                    j += 1

                # If no variable
                if j == len(segment):
                    raise InvalidFileFormatException(f"Line {i}: operator missing in {line}")
                
                # Save the variable as the rest of the segment
                variable = segment[j:]
                
                # Check the if variable starts with number or contains invalid characters
                if variable[0].isnumeric() or any(c not in valid_variables for c in variable):
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
                if len(right) == 0:
                    msg = f"Line {i}: Empty RHS in {line}"
                else:
                    msg = f"Line {i}: Invalid RHS \"{right}\" in {line}"
                raise InvalidFileFormatException(msg)
            
            eq_num += 1

        for i, eq in enumerate(equations):
            eq.append(results[i])

        return equations, vars