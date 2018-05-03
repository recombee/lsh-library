from abc import ABC, abstractmethod
"""Abstract class for write statistic file."""
class WriteFile(ABC):

    """Init the file writer.
    arguments is need with save reference for terminal print or log. """
    @abstractmethod
    def __init__(self, write_file, separator, list_of_columns, arguments, sorted=[]):
        pass

    @abstractmethod
    def write_line(self, dict_arg):
        pass

    @abstractmethod
    def get_suffix(self):
        pass

