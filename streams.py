class Stream():
    def __init__(self, name, suffix_in=".in", suffix_out=".out"):
        self.name = name
        self.suffix_in = suffix_in
        self.suffix_out = suffix_out
        self.read_file = open(name + suffix_in, "r")
        self.write_file = open(name + suffix_out, "w")

    def read(self, lenght="all"):
        if lenght == "all":
            return self.read_file.read()
        else:
            return self.read_file.read(lenght)

    def write(self, data):
        self.write_file.write(data)

    def close(self):
        self.read_file.close()
        self.write_file.close()
