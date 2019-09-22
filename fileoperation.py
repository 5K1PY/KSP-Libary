import time
from calculation import *
from parsing import *
from streams import *

class file_operator():
    def __init__(self):
        self.start_time = time.time()
        self.last_time = self.start_time
        self.streams = []

    def set_key(self, key):
        """Sets key and initializes machine."""
        self.key = key
        self.machine = ParseMachine(key)
    
    def add_stream(self, name, suffix1=".in", suffix2=".out"):
        """Adds new stream for reading and writing files."""
        self.streams.append(Stream(name, suffix1, suffix2))
    
    def check_stream(self, stream_mark):
        """Finds stream by its name or index if it exists, otherwise throws error."""
        if type(stream_mark) == str:
            if stream_mark in list(map(lambda x: x.name, self.streams)):
                return self.streams.index(stream_mark, key=lambda x: x.name)
            else:
                raise ValueError("Unknown stream.")
        elif type(stream_mark) == int:
            return stream_mark
        else:
            raise ValueError("Stream_mark should be index or name of stream.")

    def read(self, stream_mark=-1, length="all"):
        """Reads a file form stream."""
        i = self.check_stream(stream_mark)
        stream = self.streams[i]
        return stream.read(length)

    def parse(self, stream_mark=-1):
        """Parses file from stream. Returns dictionary of parsed values."""
        i = self.check_stream(stream_mark)
        stream = self.streams[i]
        return self.machine.parse(stream.read())

    def write(self, content, stream_mark=-1):
        """Writes content into a stream file."""
        i = self.check_stream(stream_mark)
        stream = self.streams[i]
        stream.write(content)

    def close(self, stream_mark=-1):
        """Closes a stream."""
        i = self.check_stream(stream_mark)
        stream = self.streams[i]
        stream.close()

    def reset(self, stream_mark=-1):
        """Resets a stream."""
        i = self.check_stream(stream_mark)
        stream = self.streams[i]
        stream.close()
        self.streams[i] = Stream(stream.name, suffix_in=stream.suffix_in, suffix_out=stream.suffix_out)

    def time(self):
        """Returns time from start."""
        return time.time() - self.last_time

k = file_operator()
k.set_key("""
|t-i
n
n: m
    m: k
    1: a
""")
k.add_stream("./data/file")
print(k.parse())
k.add_stream("./data/file1")
print(k.parse())