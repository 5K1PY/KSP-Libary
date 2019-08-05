class Counter():
    def __init__(self, expression, l="unknown"):
        self.l = l
        self.priorities = []
        self.calculations = []
        operators = ["+", "-", "*", "/", "**"]
        operator_priorities = [1, 1, 2, 2, 3]
        max_priority = max(operator_priorities) + 1
        self.variables = {}
        part = ""
        part_type = "space"
        expression += " "  # used for saving last part
        for char in expression:
            if ord("0") < ord(char) < ord("9"):
                (last_part_type, part_type) = (part_type, "number")
            elif char == "(" or char == ")":
                (last_part_type, part_type) = (part_type, "bracket")
            elif char == " ":
                (last_part_type, part_type) = (part_type, "space")
            elif ord("a") <= ord(char) <= ord("z"):
                (last_part_type, part_type) = (part_type, "variable")
            else:
                (last_part_type, part_type) = (part_type, "operator")
            
            if last_part_type == part_type:
                part += char
            else:
                if last_part_type == "number":
                    self.calculations.append((int(part), last_part_type))
                elif last_part_type == "variable":
                    self.variables[part] = None
                    self.calculations.append((part, last_part_type))
                elif last_part_type == "operator":
                    if part not in operators:
                        raise ValueError(f"Unknown operator {part} on line {self.l}.")
                    self.priorities.append(operator_priorities[operators.index(part)])
                    self.calculations.append((part, last_part_type))
                elif last_part_type == "bracket":
                    self.priorities.append(part)
                    self.calculations.append((part, last_part_type))
                part = char

    def get_variables(self):
        return self.variables
    
    def calculate(self, variables):
        for i in range(len(self.calculations)):
            if self.calculations[i][1] == "variable":
                if self.calculations[i][0] not in variables:
                    raise ValueError(f"Variable {self.calculations[i][0]} not defined.")
                if type(variables[self.calculations[i][0]]) == list:
                    try:
                        self.calculations[i] = (int(variables[self.calculations[i][0]][-1]), "number")
                    except ValueError:
                        raise TypeError(f"On line {self.l} last element of list {self.calculations[i][0]} cannot be converted to integer.")
                else:
                    try:
                        self.calculations[i] = (int(variables[self.calculations[i][0]]), "number")
                    except ValueError:
                        raise TypeError(f"On line {self.l} variable {self.calculations[i][0]} cannot be converted to integer")
        progress = []

c = Counter("11 + a*6**8 * (4+1)")
c.calculate({"a":0})
