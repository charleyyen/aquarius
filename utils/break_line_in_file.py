#! /usr/bin/python3

import getopt
import inspect
import shutil
import sys
import time

from pathlib import Path

site_list = ('indeed.com', 'LinkedIn')
class BreakLongLineInFile:
    """A class designed to parse a full patient test's serial console outputs"""
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self.debug = 1
        self.length = 70
        self.input_file = None


    def show_help(message=''):
        """Show cmdline interface"""
        message = f'{message}\n {sys.argv[0]} -i <raw_log> [-a]'
        message += f'\n    -a: When used, this tool will parse the log lines w/o datetime stamps'
        print(message)
        sys.exit(2)


    def create_new_file(self):
        """
        Create a new file whose line length is about self.length
        """
        function_name = inspect.currentframe().f_code.co_name
        if self.debug:
            print(f'In {function_name}()')
        file_handle = Path(self.input_file)
        try:
            input_file_abs_path = file_handle.resolve(strict=True)
            #print(f'input_file_abs_path: {input_file_abs_path}')
        except FileNotFoundError:
            print(f'File "{self.input_file}" does not exist!')
        else:
            with open(self.input_file, "r") as f:
                buffer = f.read().splitlines()

        print(f'buffer length: {len(buffer)}')
        file_handle = open("/tmp/aa", "w")
        i = 0
        for line in buffer:
            if len(line.strip()) <= self.length or \
                    line.lstrip().startswith("https"):
                file_handle.write(line.rstrip()+"\n")
            else:
                new_line = self.break_line(line)
                file_handle.write(new_line.rstrip()+"\n")
            i += 1

        file_handle.close()

        print(f'self.input_file: {self.input_file}')
        shutil.copyfile("/tmp/aa", self.input_file)


    def break_line(self, line):
        """
        When a line is too long (> self.length), then break it
        """
        buffer = []
        new_line = line
        while len(new_line) > self.length:
            if new_line[self.length] == " ":
                buffer.append(new_line[:self.length].strip())
                new_line = new_line[self.length:].strip()
            else:
                next_space = self.find_next_space(new_line)
                buffer.append(new_line[:next_space].strip())
                new_line = new_line[next_space:].strip()
        else:
            buffer.append(new_line.strip())

        line = "\n".join(buffer)
        return line

    def find_next_space(self, line):
        """
        When a line is too long, need to find the position of a space, which is closest to self.length
        """
        i = 1
        left_position = self.length - i
        while line[left_position] != " ":
            i -= 1
            left_position = self.length + i

        left_delta = self.length - left_position

        i = 1
        right_position = self.length + i
        while right_position < len(line) and line[right_position] != " ":
            i += 1
            right_position = self.length + i

        right_delta = right_position - self.length

        if left_delta < right_delta:
            return left_position

        return right_position


    def parse_command_line(self, argv):
        """
        Parse cmdline args. It expects '-i <input_file>'. Otherwise it'll exit out with
        a help message.
        :param argv: cmdline args. -i <input_file>: a file contains position, company name and the website name
                                   -h: display help
        """
        function_name = inspect.currentframe().f_code.co_name
        message = f'In {function_name}(), ARGV: {argv}'
        if self.debug > 1:
            print(message)

        try:
            opts, args = getopt.getopt(argv, "hi:", ["ifile="])
        except getopt.GetoptError:
            error = "cmdline opt error"
            self.show_help(error)

        if len(args) > 0:
            #print(f'==>>{args}')
            error = "Unrecognized cmdline args: " + str(argv)
            self.show_help(error)

        if opts:
            for opt, arg in opts:
                if opt == '-h':
                    message = "Showing the correct cmdline usge"
                    self.show_help()
                elif opt in ("-i", "--ifile"):
                    self.input_file = arg
                else:
                    error = "cmdline opt error" + str(argv)
                    self.show_help(error)
        else:
            error = "Missing cmdline args"
            self.show_help(error)


if __name__ == "__main__":
    obj = BreakLongLineInFile()
    obj.parse_command_line(sys.argv[1:])
    obj.create_new_file()
    #print(f'In main(): self.input_file: {obj.input_file}')
