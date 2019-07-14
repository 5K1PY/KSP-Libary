import time


class ksp_instance():
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
        self.key = []
        key = key.split("\n")
        l = "0"
        defined = {}
        for line in key:
            if line.replace(" ", "") == "":
                continue
            self.key.append([0, [], None])
            indentation = 0
            i = 0
            while line[i] == " ":
                if not line[i+1] != " ":
                    raise IndentationError("Wrong indentation on line " + l + ". Not even number of spaces.")
                i += 2
                indentation += 1
            if indentation > 0 and (line == 0 or line[-1][1] == 1):
                raise IndentationError("Wrong indentation on line " + l + ". No previous cycle.")
            if indentation > 0 and line[-1][0] + 1 < indentation:
                raise IndentationError("Wrong indentation on line " + l + ". No cycle of level 1 less on line before.")
            self.key[-1][0] = indentation

            while ":" in line[i:]:
                repeat = line[i:line.index(":", i)]
                for r in repeat:
                    if not ord("a") <= ord(r) <= ord("z"):
                        raise SyntaxError("Cannot repeat sequence " + repeat + " on line " + l + ".")
                i += len(repeat) + 1
                if repeat not in defined:
                    raise SyntaxError(repeat + " is not defined before line " + l + ".")
                self.key[-1][1].append(repeat)
            if len(self.key[-1][1]) == 0:
                self.key[-1][1] = 1

            read = line[i:]
            read = read.replace(" ", "")
            read = read.split(",")
            for r in read:
                for character in r:
                    if not ord("a") <= ord(character) <= ord("z"):
                        raise SyntaxError("Cannot repeat sequence " + repeat + " on line " + l + ".")
                if r in defined:
                    raise SyntaxError(r + " is defined earlier than on line " + l + ".")
                else:
                    defined[r] = True
            self.key[-1][2] = [(r, None) if self.key[-1][1] == 1 else (r, []) for r in read]

            l = str(int(l) + 1)

    def parse(self, file):
        self.saved = {}
        self.file = file
        stack = []
        line = 0
        while line < len(self.key):
            key = self.key[line]
            for (variable, t) in key[2]:
                self.saved[variable] = t
            if key[1] == 1:
                self.parse_line(key, line)
            else:
                if key[0] < self.key[line][0]:
                    if len(stack) + 1 == line:
                        if stack[-1][1] == stack[-1][2]:
                            line -= 1
                            stack.pop()
                            continue
                        else:
                            self.parse_line(key, line)
                            stack[-1] = (stack[-1][0], stack[-1][1], stack[-1][2] + 1)
                    else:
                        repeat = 1
                        for var in key[1]:
                            if type(self.saved[var]) == str:
                                try:
                                    repeat *= int(self.saved[var])
                                except ValueError:
                                    raise ValueError("On line " + line + " variable " + var + " cannot be converted to integer")
                            elif type(self.saved[var]) == list:
                                try:
                                    repeat *= int(self.saved[var][-1])
                                except ValueError:
                                    raise ValueError("On line " + line + " last element of list " + var + " cannot be converted to integer.")
                            elif self.saved[var] is None:
                                raise ValueError("Variable " + var + "is not in input file.")
                            if repeat == 0:
                                raise ValueError("Repeating line " + line + " zero times.")
                            self.parse_line(key, line)
                            stack.append((line, repeat, 1))

                else:
                    repeat = 1
                    for var in key[1]:
                        if type(self.saved[var]) == str:
                            try:
                                repeat *= int(self.saved[var])
                            except ValueError:
                                raise ValueError("On line " + line + " variable " + var + " cannot be converted to integer")
                        elif type(self.saved[var]) == list:
                            try:
                                repeat *= int(self.saved[var][-1])
                            except ValueError:
                                raise ValueError("On line " + line + " last element of list " + var + " cannot be converted to integer.")
                        elif self.saved[var] is None:
                            raise ValueError("Variable " + var + "is not in input file.")
                    for _ in range(repeat):
                        self.parse_line(key, line)
            line += 1

        return self.saved

    def parse_line(self, key, line):
        char = self.file.read(1)
        while char == " ":
            char = self.file.read(1)
        i = 0
        var = ""
        while char != "\n" and char != "":
            if char == " " and len(key[2]) != 1:
                while char == " ":
                    char = self.file.read(1)
                if char == "\n" or char == "":
                    continue
                if i == len(key[2]):
                    raise ValueError("More variables in file than in key on line " + line + ".")
                if key[2][i][1] is None:
                    self.saved[key[2][i][0]] = var
                else:
                    self.saved[key[2][i][0]].append(var)
                var = char
                i += 1
            else:
                var += char
            char = self.file.read(1)
        if key[2][i][1] is None:
            self.saved[key[2][i][0]] = var
        else:
            self.saved[key[2][i][0]].append(var)