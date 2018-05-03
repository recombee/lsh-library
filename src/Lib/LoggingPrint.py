import sys, traceback, logging

class LoggingPrint:
    def __init__(self, print_level, log, log_file):
        self.print_level = print_level
        logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(name)s%(asctime)s:%(levelname)s:%(message)s')
        self.log = log
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.NORMAL = '\033[0m'

    """ Status: 0 normal, 1 fail, 2 warning, 3 successful.
    Print messages and log message."""

    def p(self, *messages, sep = '', print_level = 0):
        self.do_print_info(message=self.parse_message(messages=messages, sep=sep), print_level=print_level)

    def printINFO(self, *messages, sep = '', print_level = 0):
        self.do_print_info(message=self.parse_message(messages=messages, sep=sep), print_level=print_level)

    def printWARNING(self, *messages, sep = '', print_level = 0):
        self.do_print_info(message=self.parse_message(messages=messages, sep=sep), print_level=print_level, status=2)

    def printERROR(self, *messages, sep = '', print_level = 0):
        self.do_print_info(message=self.parse_message(messages=messages, sep=sep), print_level=print_level, status=1)

    def printSUCCESS(self, *messages, sep = '', print_level = 0):
        self.do_print_info(message=self.parse_message(messages=messages, sep=sep), print_level=print_level, status=3)

    def do_print_info(self, message, print_level, status = 0):
        if self.log == "basic":
            if print_level <= 1:
                self.print_l(message=message, status=status)
        if self.log == "info":
            if print_level <= 2:
                self.print_l(message=message, status=status)
        if self.log == "debug":
            if print_level <= 4:
                self.print_l(message=message, status=status)

        if self.print_level == "basic":
            if print_level <= 0:
                self.print_w(message=message, status=status)
        if self.print_level == "info":
            if print_level <= 2:
                self.print_w(message=message, status=status)
        if self.print_level == "debug":
            if print_level <= 4:
                self.print_w(message=message, status=status)

    """ Print message to terminal."""
    def print_w(self, message, status = 0):
        if status == 0:
            print(message)
        elif status == 1:
            print(self.FAIL + message + self.NORMAL)
        elif status == 2:
            print(self.WARNING + message + self.NORMAL)
        elif status == 3:
            print(self.OKGREEN + message + self.NORMAL)
        else:
            print(self.FAIL + "ERROR: Fail status to print." + self.NORMAL)

    """ Log message to log file."""
    def print_l(self, message, status):
        if status == 0 or status == 3:
            logging.info(message)
        elif status == 1:
            logging.error(message)
        elif status == 2:
            logging.warning(message)
        elif status == 4:
            logging.debug(message)
        else:
            logging.error("ERROR: Fail status to log.")

    """ Parse messages and create one string."""
    def parse_message(self, messages, sep):
        if len(messages) == 0:
            return " "
        message = str(messages[0])
        try:
            for mes in messages[1:]:
                message = message + sep + str(mes)
        except:
            print(self.FAIL + "ERROR: Please type text in messages and separator." + self.NORMAL)
            traceback.print_exc(file=sys.stdout)
            exit(1)
        return message





