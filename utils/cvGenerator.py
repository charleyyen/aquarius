#! /usr/bin/python3

#import datetime
import getopt
import glob
import inspect
import os
import shutil
import subprocess
import sys
import time

from datetime import datetime
from pathlib import Path

site_list = ('indeed.com', 'LinkedIn')
class CvGenerator:
    """A class designed to parse a full patient test's serial console outputs"""
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self.debug = 0

        self.date_for_letter = datetime.today().strftime('%m/%d/%Y')
        self.date_for_file_prefix = datetime.today().strftime('%Y_%m_%d')
        #print(f"Today: {self.date_for_letter}")
        #print(f"Prefix: {self.date_for_file_prefix}")

        self.template_cover_letter = "/home/cyan/Documents/jobs/02_out/template_cover_letter.txt"
        with open(self.template_cover_letter) as f:
            self.buffer = f.read().splitlines()

        #print(f'Length: {len(self.buffer)}, self.template_cover_letter: {self.template_cover_letter}')

        self.archived_dir =  "/home/cyan/Documents/jobs/01_applied_list/"
        self.archived_list = self.archived_dir + self.date_for_file_prefix + "_00_list"
        self.input_file = None
        self.archived_cover_letter = None


    def show_help(message=''):
        """Show cmdline interface"""
        message = f'{message}\n {sys.argv[0]} -i <raw_log> [-a]'
        message += f'\n    -a: When used, this tool will parse the log lines w/o datetime stamps'
        print(message)
        sys.exit(2)

    def applied_already(self, key_name):
        file_with_pattern1 = self.archived_dir + "*" + key_name + "*.pdf"
        file_with_pattern2 = self.archived_dir + "*" + key_name.lower() + "*.pdf"
        if glob.glob(file_with_pattern1):
            print(f'Already applied "{key_name}":\n{file_with_pattern1}\n')
            return True
        if glob.glob(file_with_pattern2):
            print(f'Already applied "{key_name}":\n{file_with_pattern2}\n')
            return True

        return False

    def create_letter(self):
        function_name = inspect.currentframe().f_code.co_name
        file_handle = Path(self.input_file)
        try:
            input_file_abs_path = file_handle.resolve(strict=True)
            #print(f'input_file_abs_path: {input_file_abs_path}')
        except FileNotFoundError:
            print(f'File "{self.input_file}" does not exist!')
        else:
            with open(self.input_file, "r") as open_for_read:
                site_name = None
                for line in open_for_read.readlines():
                    if line[0] == "#" or len(line.strip()) == 0:
                        continue
                    if "https" in line:
                        for site in site_list:
                            if site.lower() in line:
                                site_name = site
                        continue

                    list_ = line.rstrip().split(",")
                    #print(f'Length: {len(list_)}, #{list_}#\n{line}\n')
                    assert len(list_) == 2
                    key_name = "_".join(list_[1].strip().split())
                    key_name = key_name.replace("'", "") # remove single quote from company name
                    new_cover_letter = self.archived_dir + self.date_for_file_prefix + "_" + key_name.lower() + ".txt"
                    new_cover_letter_pdf = new_cover_letter.replace("txt", "pdf")
                    print(f'##==-->>new_cover_letter PDF: {new_cover_letter.replace("txt", "pdf")}')
                    if self.applied_already(key_name):
                        continue

                    assert site_name
                    list_.append(site_name)

                    print(f'new_cover_letter TXT: {new_cover_letter}')
                    file_handle = open(new_cover_letter, "w")
                    for line in self.buffer:
                        if "__DATE__" in line:
                            line = self.date_for_letter
                        elif "__POS__" in line:
                            line = line.replace("__POS__", list_[0].strip())
                            line = line.replace("__CO__", list_[1].strip())
                            line = line.replace("__SITE__", list_[2].strip())

                        file_handle.write(line + "\n")
                    file_handle.write("\n")
                    file_handle.close()

                    command = f"libreoffice --convert-to pdf --outdir {self.archived_dir} {new_cover_letter}"
                    print(f'{command}')
                    child = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
                    streamdata = child.communicate()[0]
                    loop = 0
                    while child.returncode != 0 and loop < 3:
                        child = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
                        streamdata = child.communicate()[0]
                        print(f'child.returncode: {child.returncode}')
                        time.sleep(1)
                        loop += 1
                    if os.path.isfile(new_cover_letter_pdf):
                        print(f'new_cover_letter PDF: {new_cover_letter.replace("txt", "pdf")}')
                    else:
                        print(f'Failed to create {new_cover_letter_pdf}')


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
            opts, args = getopt.getopt(argv, "hi:a", ["ifile=", "all"])
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
                    shutil.copyfile(self.input_file, self.archived_list)
                else:
                    error = "cmdline opt error" + str(argv)
                    self.show_help(error)
        else:
            error = "Missing cmdline args"
            self.show_help(error)


if __name__ == "__main__":
    obj = CvGenerator()
    obj.parse_command_line(sys.argv[1:])
    obj.create_letter()
    #print(f'In main(): self.input_file: {obj.input_file}')
