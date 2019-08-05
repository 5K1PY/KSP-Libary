import time


class file_read_instance():
    def __init__(self, file_name):
        self.start_time = time.time()
        self.last_time = self.start_time
        self.file_name = file_name

    def read(self, suffix=".in"):
        """Starts reading. Returns read file."""
        self.read_file = open(self.file_name + suffix, "r")
        return self.read_file

    def parse(self, key, suffix=".in"):
        """Parses file. Returns dictionary of parsed values."""
        self.read_file = open(self.file_name + suffix, "r")
        return ParseMachine(key).parse(self.read_file)

    def write(self, suffix=".out"):
        """Starts writing. Returns write file."""
        self.write_file = open(self.file_name + suffix, "w")
        return self.write_file

    def both(self, suffix1=".in", suffix2=".out"):
        """Starts both reading and writing.
        Returns both read and write file."""
        return (self.read(suffix1), self.write(suffix2))

    def close_r(self):
        """Ends reading."""
        self.read_file.close()

    def close_w(self):
        """Ends writing."""
        self.write_file.close()

    def close_b(self):
        """Ends both reading and writing."""
        self.close_r()
        self.close_w()

    def reset(self):
        """Resets time"""
        self.last_time = time.time()

    def time(self):
        """Returns time from start."""
        return time.time() - self.last_time

class ParseMachine():
    def __init__(self, key):
        """Creates instructions to interpret key"""
        self.key = []
        key = key.split("\n")
        self.settings = {  # settings
            "indentation": ("s4", ("s2", "s4", "s8", "t")),  # indentation: s2 - 2 spaces, s4 - 4 spaces, s8 - osm spaces, t - tabs 
            "type": ("s", ("s", "i", "f"))}  # type of input: s - string, i - int, f - float
        self.settings_names = {}
        for setting in self.settings:
            self.settings_names[setting[0]] = setting
        l = "0"
        defined = {}
        applied_settings = False
        for line in key:
            if line.replace(" ", "") == "":
                continue  # skip empty line
            
            if applied_settings is False:  # appling settings needed before indentation
                self.apply_settings()
                applied_settings = True
            
            self.key.append([0, [], None])
            
            (i, indentation) = self.get_indentation(line, l)
            if indentation > 0 and l == 0:  # getting indentation
                raise IndentationError("Wrong indentation on line " + l + ". No previous cycle.")
            if indentation > 0 and self.key[-2][0] + 1 < indentation:
                raise IndentationError("Wrong indentation on line " + l + ". No cycle of level 1 less on line before.")
            self.key[-1][0] = indentation

            if line[i] == "|":  # changing settings
                self.set_settings(line)
                self.key.pop()
                applied_settings = False
                continue
            
            if line.count(":") == 0:  # getting repeat
                self.key[-1][1] = BlankCalculator()
            elif line.count(":") == 1:
                repeat = line[i:line.index(":")]
                i += len(repeat) + 1
                self.key[-1][1] = Calculator(repeat, l)
            else:
                raise SyntaxError(f"More than one : on line {l}.")

            read = line[i:]
            setting = None
            if "|" in line[i:]:  # splitting setting and reading parts
                (read, setting) = (line[i:line.index("|", i)], line[line.index("|", i)+1:])
            read = read.replace(" ", "").split(",")

            for variable in read:
                for character in variable:  # finding user errors
                    if not ord("a") <= ord(character) <= ord("z"):
                        raise SyntaxError("Cannot repeat sequence " + repeat + " on line " + l + ".")
                if variable in defined:
                    raise SyntaxError(variable + " is defined earlier than on line " + l + ".")
                else:
                    defined[variable] = True
            self.key[-1][2] = [[r, None, self.default_type] if isinstance(self.key[-1][1], BlankCalculator) and self.key[-1][0] == 0 else [r, [], self.default_type] for r in read]

            if setting is not None:
                setting = setting.replace(" ","").split(",")
                i = 0
                if len(setting) < len(self.key[-1][2]):
                    raise ValueError("Not enough settings on line " + l + ".")
                if len(setting) > len(self.key[-1][2]):
                    raise ValueError("Too many settings on line " + l + ".")
                for s in setting:
                    if s == "s":
                        read_type = str
                    elif s == "i":
                        read_type = int
                    elif s == "f":
                        read_type = float
                    else:
                        raise ValueError("Unknown value on line " + l + ": " + s)
                    self.key[-1][2][i][2] = read_type
                    i += 1
                
    
            l = str(int(l) + 1)
        self.key.append([0, None])

    def set_settings(self, line):
        """Updates all settings"""
        line = line.split("|")
        for part in line:
            if part.replace(" ", "") == "":
                continue
            (setting, value) = part.replace(" ", "").split("-")
            if setting in self.settings_names:
                setting = self.settings_names[setting]
            elif setting not in self.settings:
                raise ValueError("Not known setting: " + setting)
            if value not in self.settings[setting][1]:
                raise ValueError("Unknown value: " + value)
            else:
                self.settings[setting] = (value, self.settings[setting][1])
    
    def apply_settings(self):
        """Apllies all settings"""
        for (setting, value) in self.settings.items():
            value = value[0]
            if setting == "type":  # aktualization of settings
                if value == "s":
                    self.default_type = str
                elif value == "i":
                    self.default_type = int
                elif value == "f":
                    self.default_type = float
            elif setting == "indentation":
                if value == "s2":
                    self.indentation = " " * 2
                elif value == "s4":
                    self.indentation = " " * 4
                elif value == "s8":
                    self.indentation = " " * 8
                elif value == "t":
                    self.indentation = "\t"

    def get_indentation(self, line, l="unknown"):
        """Gets indentation for line. l number line parametr"""
        i = 0
        indentation_count = 0
        while line[i] == self.indentation[0]:
            if len(line) - i < len(self.indentation) or line[i: i+len(self.indentation)] != self.indentation:
                raise IndentationError("Wrong indentation on line " + l + ".")
            i += len(self.indentation)
            indentation_count += 1
        return (i, indentation_count)

    def parse(self, file):
        """Parses key by its instructions."""
        self.saved = {}
        self.file = file
        stack = []
        line = 0
        while line < len(self.key):
            key = self.key[line]
            if key[1] is None:
                break
            
            repeat = key[1].calculate(self.saved)  # determaning number of repeats
            if repeat == 0:
                raise ValueError(f"Repeating line {line} zero times.")
            elif repeat < 0:
                raise ValueError(f"Repeating line {line} less than zero times.")
            elif repeat % 1 != 0:
                raise ValueError(f"Repeating line {line} not whole number of times.")
            
            if key[2][0][0] not in self.saved:  # defining variables
                for (variable, t, _) in key[2]:
                    if t == []:
                        self.saved[variable] = []
                    else:
                        self.saved[variable] = None

            
            if line + 1 != len(self.key) and key[0] < self.key[line + 1][0]:  # cycle with cylce in itself
                if len(stack) != 0 and stack[-1][0] == line:
                    if stack[-1][1] == stack[-1][2]:  # returning from cycle
                        line = stack[-1][3]
                        stack.pop()
                        continue
                    else:  # next iteration
                        self.parse_line(key, line)
                        stack[-1][2] += 1
                else:  # creating new repetition
                    self.parse_line(key, line)
                    l = line + 1
                    while key[0] < self.key[l][0]:
                        l += 1
                    if line == 0 or self.key[l][0] >= self.key[line-1][0]:
                        stack.append([line, repeat, 1, l])
                    else:
                        stack.append([line, repeat, 1, line-1])


            else:  # cycle without cycle in itself
                for _ in range(repeat):  # execution of one level cycle
                    self.parse_line(key, line)
                if len(stack) > 0:  # going next same level cycle
                    if key[0] == self.key[line+1][0]: 
                        line += 1
                        continue
                    else:  # returning from cycle
                        line = stack[-1][0]
                        continue
            line += 1

        return self.saved

    def parse_line(self, key, line):
        """Reads line."""
        char = self.file.read(1)
        i = 0
        var = ""
        while char != "\n" and char != "":
            if char == " " and len(key[2]) != 1:
                while char == " ":
                    char = self.file.read(1)  # finds next non-space character
                if char == "\n" or char == "":
                    break
                if i >= len(key[2]):
                    raise ValueError("More variables in file than in key on line " + line + ".")
                try:  # apllies types on found varibles
                    if key[2][i][1] != []:
                        self.saved[key[2][i][0]] = key[2][i][2](var)
                    else:
                        self.saved[key[2][i][0]].append(key[2][i][2](var))
                except ValueError:
                    raise ValueError(var + " cannot be converted.")
                var = char
                i += 1
            else:
                var += char
            char = self.file.read(1)
        if i >= len(key[2]):
            raise ValueError("More variables in file than in key on line " + line + ".")
        try:
            if key[2][i][1] != []:
                self.saved[key[2][i][0]] = key[2][i][2](var)
            else:
                self.saved[key[2][i][0]].append(key[2][i][2](var))
        except ValueError:
            raise ValueError(var + " cannot be converted.")
        return None

class Calculator():
    def __init__(self, expression, l="unknown"):
        """Does pre-calculations for computing expression with variables. Line parameter l for errors."""
        self.l = l
        self.priorities = []
        self.calculations = []
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
                    self.calculations.append((int(part)*positivity_multiplier, last_part_type))
                    positivity_multiplier = 1
                elif last_part_type == "variable":
                    if char == "(" or part_type == "number" or positivity_multiplier == -1:
                        raise SyntaxError(f"Invalid expression on line {self.l}.")
                    self.variables[part] = None
                    self.calculations.append((part, last_part_type))
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
                        self.calculations.append((part, last_part_type))
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
                    self.calculations.append((part, last_part_type))
                part = char
        if bracket_count > 0:
            raise SyntaxError(f"Invalid bracketing on line {self.l}")

    def get_variables(self):
        """Returns variables needed for expression."""
        return self.variables
    
    def calculate(self, variables):
        """Calculate value of expression for variables."""
        for i in range(len(self.calculations)):  # replaces variables with their values
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
        last_operator = 0
        for c in self.calculations:  # calculates expression
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
    def calculate(self, variables):
        return 1
