from .ABCWriteFile import WriteFile

""" Class for printing CSV from dictionaries. For creating plots."""
class WriteFileCSV(WriteFile):

    def __init__(self, write_file, separator, list_of_columns, arguments, sorted=[]):
        self.head = []
        self.separator = separator
        self.sorted = sorted
        self.to_print = []
        try:
            self.file = open(write_file + ".csv", "a")
        except:
            arguments["logp"].printERROR("Cant not create output file:", write_file + ".csv")
            exit(1)
        count = len(list_of_columns)
        for item in list_of_columns:
            count -= 1
            self.head.append(item)
            self.file.write(str(item))
            if (count != 0):
                self.file.write(str(self.separator))
        self.file.write("\n")

    """ Write one line with stats from results."""
    def write_line(self, dict):
        if len(self.sorted) != 0:
            to_write = []
            for item in self.head:
                if item in dict:
                    to_write.append(dict[item])
                else:
                    to_write.append(False)
            self.to_print.append(to_write)
        else:
            count = len(self.head)
            for item in self.head:
                count -= 1
                if item in dict:
                    self.file.write(str(dict[item]))
                if (count != 0):
                    self.file.write(str(self.separator))
            self.file.write("\n")

    def get_suffix(self):
        return ".csv"

    def __del__(self):
        if len(self.sorted) != 0:
            try:
                for i in range(len(self.sorted)):
                    self.to_print.sort(key=lambda x: (
                    x[[j for j, x in enumerate(self.head) if x == self.sorted[len(self.sorted) - i - 1]][0]]))
                for i in self.to_print:
                    self.file.write(self.separator.join([str(j) for j in i]))
                    self.file.write("\n")
            except:
                print("Bad arguments to sorted out print in csv.")
                exit(1)
        try:
            self.file.close()
        except:
            exit(1)
