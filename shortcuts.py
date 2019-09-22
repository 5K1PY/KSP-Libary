from fileoperation import *

class parse_manager():
    def __init__(self, key, file_names, file_input_suffixes=None, file_output_suffixes=None, parallel=False):
        self.f = file_operator()
        self.f.set_key(key)
        if file_input_suffixes == None:
            file_input_suffixes = [".in"] * len(file_names)
        if file_output_suffixes == None:
            file_output_suffixes = [".in"] * len(file_names)
        self.file_names = file_names
        self.file_input_suffixes = file_input_suffixes
        self.file_output_suffixes = file_output_suffixes
        self.file_index = 0
        self.parallel = parallel
        if self.parallel is True:
            for i in range(len(file_names)):
                k.add_stream(file_names[i], suffix1=file_input_suffixes[i], suffix2=file_output_suffixes[i])
    
    def read(self):
        if self.parallel is True:
            raise Exception("Parallel reading is set on.")
        if self.file_index != 0:
            self.f.close()
        self.f.add_stream(self.file_names[self.file_index], suffix1=self.file_input_suffixes[self.file_index], suffix2=self.file_output_suffixes[self.file_index])
        self.file_index += 1
        return self.f.parse()

    def write(self, text):
        if self.parallel is True:
            raise Exception("Parallel writing is set on.")
        self.f.write(text)
    
    def read_parallel(self, index):
        if self.parallel is True:
            raise Exception("Parallel reading is set off.")
        return self.f.parse(stream_mark=index)

    def write_parallel(self, text, index):
        if self.parallel is True:
            raise Exception("Parallel writing is set off.")
        self.f.write(text, stream_mark=index)
