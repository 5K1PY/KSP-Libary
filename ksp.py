import time


class ksp_instance():
    def __init__(self, file_name):
        self.start_time = time.time()
        self.file_name = file_name

    def read(self, suffix=".in"):
        """Starts reading. Returns read file."""
        self.read_file = open(self.file_name + suffix, "r")
        return self.read_file

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
        self.start_time = time.time()

    def time(self):
        """Returns time from start."""
        return time.time() - self.start_time
