from ksp.fileoperation import *

class parse_manager():
    def __init__(self, key, file_names, file_input_suffixes=None, file_output_suffixes=None, parallel=False):
        """
        Creates itself.

        Arguments:
        key {str} -- Key for file reading
        file_names {list} -- Names of files for reading and writing
        file_input_suffixes {list} -- Suffixes of files for reading
        file_output_suffixes {list} -- Suffixes of files for writing
        parallel {bool} -- if reading and writing into multiple files at once is possible
        """
        
        self.f = file_operator()
        self.f.set_key(key)
        if file_input_suffixes == None:
            file_input_suffixes = [".in"] * len(file_names)
        if file_output_suffixes == None:
            file_output_suffixes = [".out"] * len(file_names)
        self.file_names = file_names
        self.file_input_suffixes = file_input_suffixes
        self.file_output_suffixes = file_output_suffixes
        self.file_index = 0
        self.parallel = parallel
        if self.parallel is True:
            for i in range(len(file_names)):
                self.f.add_stream(file_names[i], suffix1=file_input_suffixes[i], suffix2=file_output_suffixes[i])
    
    def read(self):
        """
        Reads next file.
        
        Returns:
        string
        """
        if self.parallel is True:
            raise Exception("Parallel reading is set on.")
        if self.file_index != 0:
            self.f.close()
        self.f.add_stream(self.file_names[self.file_index], suffix1=self.file_input_suffixes[self.file_index], suffix2=self.file_output_suffixes[self.file_index])
        self.file_index += 1
        return self.f.read()

    def parse(self):
        """
        Parses next file.
        
        Returns:
        dictionary
        """
        if self.parallel is True:
            raise Exception("Parallel reading is set on.")
        if self.file_index != 0:
            self.f.close()
        self.f.add_stream(self.file_names[self.file_index], suffix1=self.file_input_suffixes[self.file_index], suffix2=self.file_output_suffixes[self.file_index])
        self.file_index += 1
        return self.f.parse()

    def write(self, text):
        """
        Writes into next file.
        
        Arguments:
        text {str} -- what should be in file
        """
        if self.parallel is True:
            raise Exception("Parallel writing is set on.")
        self.f.write(text)
    
    def read_parallel(self, file):
        """
        Reads given file.
        
        Arguments:
        file {int or str} -- name of file or index of file in file_names
        
        Returns:
        string
        """
        
        if self.parallel is False:
            raise Exception("Parallel reading is set off.")
        return self.f.parse(stream_mark=file)

    def parse_parallel(self, file):
        """
        Parses given file.
        
        Arguments:
        file {int or str} -- name of file or index of file in file_names
        
        Returns:
        dictionary
        """
        
        if self.parallel is False:
            raise Exception("Parallel reading is set off.")
        return self.f.parse(stream_mark=file)

    def write_parallel(self, text, file):
        """
        Writes into given file.
        
        Arguments:
        text {str} -- what should be in file
        file {int or str} -- name of file or index of file in file_names
        """
        
        if self.parallel is False:
            raise Exception("Parallel writing is set off.")
        self.f.write(text, stream_mark=file)
