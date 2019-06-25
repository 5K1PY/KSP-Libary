class ParseMachine():
    def __init__(self, file, key):
        self.file = file
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
                repeat = line[i:line.index(":")]
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
                    raise NotImplementedError()
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
                        else:
                            raise NotImplementedError()
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


p = ParseMachine("f", """
n, m
n: a
m: b
""")
p.parse(open("file.in", "r"))
