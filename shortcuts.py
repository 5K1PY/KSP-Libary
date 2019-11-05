from ksp.fileoperation import *
from ksp.progressbar import *


class FileManager():
    def __init__(self, key, file_names, file_input_suffixes=None, file_output_suffixes=None, parallel=False, progressbar=False):
        """
        Creates itself.

        Arguments:
        key {str} -- Key for file reading
        file_names {list} -- Names of files for reading and writing
        file_input_suffixes {list} -- Suffixes of files for reading
        file_output_suffixes {list} -- Suffixes of files for writing
        parallel {bool} -- if reading and writing into multiple files at once is possible
        progressbar {bool} -- if progressbar should be displayed (cannot be used with parallel on)
        """

        self.files = FileOperator()
        self.files.set_key(key)
        if file_input_suffixes is None:
            file_input_suffixes = [".in"] * len(file_names)
        if file_output_suffixes is None:
            file_output_suffixes = [".out"] * len(file_names)
        self.file_names = file_names
        self.file_input_suffixes = file_input_suffixes
        self.file_output_suffixes = file_output_suffixes
        self.file_index = 0
        self.parallel = parallel
        self.progressbar = ProgressBar(40) if progressbar is True else None
        if self.parallel is True:
            if self.progressbar is not None:
                raise ValueError("Progressbar cannot be set on while parallel read and write is.")
            for i in range(len(file_names)):
                self.files.add_stream(file_names[i], suffix1=file_input_suffixes[i], suffix2=file_output_suffixes[i])

    def read(self):
        """
        Reads next file.

        Returns:
        string
        """
        if self.parallel is True:
            raise Exception("Parallel reading is set on.")
        if self.file_index != 0:
            self.files.close()

        if self.progressbar is not None:
            if self.file_index > 0:
                self.progressbar.end_bar(f"Finished working on {self.file_names[self.file_index-1]}")
            self.progressbar.display_bar(0, f"Working on {self.file_names[self.file_index]}")

        self.files.add_stream(self.file_names[self.file_index], suffix1=self.file_input_suffixes[self.file_index], suffix2=self.file_output_suffixes[self.file_index])
        self.file_index += 1

        return self.files.read()

    def parse(self):
        """
        Parses next file.

        Returns:
        dictionary
        """
        if self.parallel is True:
            raise Exception("Parallel reading is set on.")
        if self.file_index != 0:
            self.files.close()
        self.files.add_stream(
            self.file_names[self.file_index],
            suffix1=self.file_input_suffixes[self.file_index],
            suffix2=self.file_output_suffixes[self.file_index])
        self.file_index += 1
        return self.files.parse()

    def write(self, text):
        """
        Writes into next file.

        Arguments:
        text {str} -- what should be in file
        """
        if self.parallel is True:
            raise Exception("Parallel writing is set on.")
        self.files.write(text)

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
        return self.files.parse(stream_mark=file)

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
        return self.files.parse(stream_mark=file)

    def write_parallel(self, text, file):
        """
        Writes into given file.

        Arguments:
        text {str} -- what should be in file
        file {int or str} -- name of file or index of file in file_names
        """
        if self.parallel is False:
            raise Exception("Parallel writing is set off.")
        self.files.write(text, stream_mark=file)

    def update_progressbar(self, part):
        """
        Updates progress bar.

        Arguments:
        part {float} -- How much of the progress bar should be filled
        """
        if self.progressbar is None:
            raise ValueError("Progressbar is turned off.")
        self.progressbar.display_bar(part, f"Working on {self.file_names[self.file_index]}")

    def end(self):
        """
        Ends self (closes all files etc.)
        """
        if self.parallel is True:
            for i in range(len(self.files.streams)):
                self.files.close(i)
        else:
            self.files.close()
        self.progressbar.end_bar(f"Finished working on {self.file_names[self.file_index-1]}")
