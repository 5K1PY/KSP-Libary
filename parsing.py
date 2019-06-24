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
                if defined[r] is True:
                    raise SyntaxError(r + " is defined earlier than on line " + l + ".")
                else:
                    defined[r] = True
            self.key[-1][2] = [(r, None) if self.key[-1][1] == 1 else (r, []) for r in read]

            l = str(int(l) + 1)

    def parse(self):
        saved = {}
        for key in self.key:
            for (variable, t) in key[2]:
                saved[variable] = t
            i = 0
            if key[2] == 1:
                pass
            else:
                pass

p = ParseMachine("f", "n, m\n\nn: a\nm: b")
