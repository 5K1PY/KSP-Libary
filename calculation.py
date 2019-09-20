class Calculator():
    def __init__(self, expression, l="unknown"):
        """Does pre-calculations for computing expression with variables. Line parameter l for errors."""
        self.l = l
        self.priorities = []
        self.precalculations = []
        operators = ["+", "-", "*", "/", "**"]
        operator_priorities = [1, 1, 2, 2, 3]
        self.variables = {}
        bracket_count = 0
        part = ""
        part_type = None
        expression = "(" + expression.replace(" ", "") + "):"
        positivity_multiplier = 1
        for char in expression:
            if ord("0") <= ord(char) <= ord("9"):  # analyzing new character
                (last_part_type, part_type) = (part_type, "number")
            elif char == ":":
                (last_part_type, part_type) = (part_type, "end")
            elif char == "(" or char == ")":
                (last_part_type, part_type) = (part_type, "bracket")
            elif ord("a") <= ord(char) <= ord("z"):
                (last_part_type, part_type) = (part_type, "variable")
            else:
                (last_part_type, part_type) = (part_type, "operator")
            
            if last_part_type == part_type and part_type != "bracket":
                part += char
            else:  # saving last part
                if last_part_type == "number":
                    if char == "(" or part_type == "variable":
                        raise SyntaxError(f"Invalid expression on line {self.l}.")
                    self.precalculations.append((int(part)*positivity_multiplier, last_part_type))
                    positivity_multiplier = 1
                elif last_part_type == "variable":
                    if char == "(" or part_type == "number" or positivity_multiplier == -1:
                        raise SyntaxError(f"Invalid expression on line {self.l}.")
                    self.variables[part] = None
                    self.precalculations.append((part, last_part_type))
                elif last_part_type == "operator":
                    if positivity_multiplier == -1:
                        if part != "-":
                            positivity_multiplier = 1
                    if positivity_multiplier == 1:
                        if char == ")":
                            raise SyntaxError(f"Invalid expression on line {self.l}.")
                        if part not in operators:
                            raise ValueError(f"Unknown operator {part} on line {self.l}.")
                        self.priorities.append(operator_priorities[operators.index(part)])
                        self.precalculations.append((part, last_part_type))
                elif last_part_type == "bracket":
                    if part == "(":
                        if char == "-":
                            positivity_multiplier = -1
                        elif char == ")" or part_type == "operator" or positivity_multiplier == -1:
                            raise SyntaxError(f"Invalid expression on line {self.l}.")
                        bracket_count += 1
                        self.priorities.append(part)
                    else:
                        if char == "(" or part_type == "number" or part_type == "variable" or positivity_multiplier == -1:
                            raise SyntaxError(f"Invalid expression on line {self.l}.")
                        bracket_count -= 1
                        if bracket_count < 0:
                            raise SyntaxError(f"Invalid bracketing on line {self.l}")
                    self.precalculations.append((part, last_part_type))
                part = char
        if bracket_count > 0:
            raise SyntaxError(f"Invalid bracketing on line {self.l}")

    def get_variables(self):
        """Returns variables needed for expression."""
        return self.variables
    
    def calculate(self, variables, list_watch):
        """Calculate value of expression for variables."""
        calculations = self.precalculations[:]
        for i in range(len(calculations)):  # replaces variables with their values
            if calculations[i][1] == "variable":
                if calculations[i][0] not in variables:
                    raise ValueError(f"Variable {calculations[i][0]} not defined.")
                if calculations[i][0] in list_watch:    
                    try:
                        calculations[i] = (int(list_watch[calculations[i][0]][1][-1][1][-1]), "number")
                    except ValueError:
                        raise TypeError(f"On line {self.l} last element of lists {calculations[i][0]} cannot be converted to integer.")
                elif type(variables[calculations[i][0]]) == list:
                    try:
                        calculations[i] = (int(variables[calculations[i][0]][-1]), "number")
                    except ValueError:
                        raise TypeError(f"On line {self.l} last element of list {calculations[i][0]} cannot be converted to integer.")
                else:
                    try:
                        calculations[i] = (int(variables[calculations[i][0]]), "number")
                    except ValueError:
                        raise TypeError(f"On line {self.l} variable {calculations[i][0]} cannot be converted to integer")
        progress = []
        last_operator = 0
        for c in calculations:  # calculates expression
            if c[1] == "number":
                progress.append(c[0])
            elif c[1] == "operator":
                if last_operator > 0 and self.priorities[last_operator-1] != "(" and self.priorities[last_operator-1] >= self.priorities[last_operator]:
                    result = self.compute(progress[-3:])
                    for _ in range(3):
                        progress.pop()
                    progress.append(result)
                progress.append(c[0])
                last_operator += 1
            elif c[1] == "bracket":
                if c[0] == "(":
                    progress.append(c[0])
                    last_operator += 1
                elif c[0] == ")":
                    while progress[-2] != "(":
                        result = self.compute(progress[-3:])
                        for _ in range(3):
                            progress.pop()
                        progress.append(result)
                    progress.pop(-2)
        return progress[0]

    def compute(self, commands):
        """Computes value of operation."""
        (number1, operator, number2) = commands
        if operator == "+":
            return number1 + number2
        elif operator == "-":
            return number1 - number2
        elif operator == "*":
            return number1 * number2
        elif operator == "/":
            if number2 == 0:
                raise ZeroDivisionError(f"Division by zero on line {self.l}")
            return number1 / number2
        elif operator == "**":
            return number1 ** number2

class BlankCalculator():
    def calculate(self, variables, list_watch):
        return 1