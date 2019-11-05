import sys


class ProgressBar():
    def __init__(self, length, start="|", end="|", full="█", empty=" ", show_percentage=True):
        """
        Creates itself.

        Arguments:
        length {int} -- Number of characters in progress bar
        start {str} -- What progress bars starts with
        end {str} -- What progress bars ends with
        full {str} -- How should look like full parts of progress bar
        empty {str} -- How should look like empty parts of progress bar
        show_percentage {bool} -- If percentage should be seen after progress bar
        """
        self.length = length
        self.start = start
        self.end = end
        self.full = full
        self.empty = empty
        self.show_percantage = show_percentage
        self.min_length = 0

    def display_bar(self, part, text=""):
        """
        Displays progress bar.

        Arguments:
        part {int, float} -- Part of progress bar which should be filled
        text {str} -- Text which should be displayed before progress bar
        """
        if not isinstance(part, (int, float)):
            raise TypeError("Part should be int or float between 0 and 1.")
        if not isinstance(text, str):
            text = str(text)
        if 0 <= part and part <= 1:
            if text != "":
                text += " "
            text += f"{self.start}{self.full*(round(part * self.length))}"  # add start and fulled part of progress bar
            text += f"{self.empty*(self.length-round(part * self.length))}{self.end}"  # add empty part and end of progress bar
            if self.show_percantage:
                text += f" {round(100 * part)}%"  # add percentage
            if len(text) < self.min_length:
                text += " "*(self.min_length - len(text))
            print(text, end="\r")
            self.min_length = max(self.min_length, len(text))
            sys.stdout.flush()
        else:
            raise ValueError("Part should be between 0 and 1.")

    def end_bar(self, text=""):
        """
        Displays full progress bar with newline on end.

        Arguments:
        text {str} -- Text which should be displayed before progress bar
        """
        if not isinstance(text, str):
            text = str(text)
        if text != "":
            text += " "
        text += f"{self.start}{self.full*(self.length)}{self.end}"
        if self.show_percantage is True:
            text += " 100%"
        if len(text) < self.min_length:
            text += " "*(self.min_length - len(text))
        print(text)
        sys.stdout.flush()
