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
            
            while ":" in line[i:]:  # getting repeat
                repeat = line[i:line.index(":", i)]
                for r in repeat:
                    if not ord("a") <= ord(r) <= ord("z"):
                        raise SyntaxError("Invalid character for variable " + repeat + " on line " + l + ".")
                i += len(repeat) + 1
                if repeat not in defined:
                    raise SyntaxError(repeat + " is not defined before line " + l + ".")
                self.key[-1][1].append(repeat)
            if len(self.key[-1][1]) == 0:
                self.key[-1][1] = 1

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
                    raise SyntaxError(r + " is defined earlier than on line " + l + ".")
                else:
                    defined[variable] = True
            self.key[-1][2] = [[r, None, self.default_type] if self.key[-1][1] == 1 and self.key[-1][0] == 0 else [r, [], self.default_type] for r in read]

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
            if key[2][0][0] not in self.saved:  # defining vyriables
                for (variable, t, _) in key[2]:
                    if t == []:
                        self.saved[variable] = []
                    else:
                        self.saved[variable] = None
            if key[1] == 1:  # line without repeating
                self.parse_line(key, line)
                if len(stack) > 0:
                    if key[0] == self.key[line+1][0]: 
                        line += 1
                        continue
                    else:
                        line = stack[-1][0]
                        continue
            else:  # opakování řádku vícekrát
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
                        repeat = 1
                        for var in key[1]:
                            if type(self.saved[var]) != list:
                                try:
                                    repeat *= int(self.saved[var])
                                except ValueError:
                                    raise TypeError("On line " + line + " variable " + var + " cannot be converted to integer")
                            elif type(self.saved[var]) == list:
                                try:
                                    repeat *= int(self.saved[var][-1])
                                except ValueError:
                                    raise TypeError("On line " + line + " last element of list " + var + " cannot be converted to integer.")
                            elif self.saved[var] is None:
                                raise ValueError("Variable " + var + "is not in input file.")
                            if repeat == 0:
                                raise ValueError("Repeating line " + line + " zero times.")
                            self.parse_line(key, line)
                            l = line + 1
                            while key[0] < self.key[l][0]:
                                l += 1
                            if line == 0 or self.key[l][0] >= self.key[line-1][0]:
                                stack.append([line, repeat, 1, l])
                            else:
                                stack.append([line, repeat, 1, line-1])


                else:  # cycle without cycle in itself
                    repeat = 1
                    for var in key[1]:  # determaning number of repeats
                        if type(self.saved[var]) != list:
                            try:
                                repeat *= int(self.saved[var])
                            except ValueError:
                                raise TypeError("On line " + line + " variable " + var + " cannot be converted to integer")
                        elif type(self.saved[var]) == list:
                            try:
                                repeat *= int(self.saved[var][-1])
                            except ValueError:
                                raise TypeError("On line " + line + " last element of list " + var + " cannot be converted to integer.")
                        elif self.saved[var] is None:
                            raise ValueError("Variable " + var + "is not in input file.")
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
        i += 1
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

p = ParseMachine("""
|t-i
n
n: a
""")
print(p.parse(open("DataFiles/file.in", "r")))
