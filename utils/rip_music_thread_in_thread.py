#! /usr/bin/python3
"""
A standalone tool to parse a full patient test's serial console outputs
youtube-dl --extract-audio --audio-format mp3 -o "%(title)s.%(ext)s" http://www.youtube.com/watch?v=rtOvBOTyX00o
youtube-dl -x --audio-quality 0 -f bestaudio --restrict-filenames --audio-format \
        mp3 -o "/tmp/qq/%(title)s.%(ext)s" --no-part https://www.youtube.com/watch?v=6QORyIWN7JI
"""

import getopt
import glob
import inspect
import os
import subprocess
import sys
import tempfile
import threading
import time

from collections import defaultdict
from datetime import date
from multiprocessing.pool import ThreadPool as Pool

DEST = '/home/cyan/Music/dest/'
#DEST = '/tmp/'
RIP = 'youtube-dl -x --audio-quality 0 -f bestaudio --restrict-filenames --audio-format mp3 '
# When '-k' is used, the webm files is kept
#RIP = 'youtube-dl -k -x --audio-quality 0 -f bestaudio --restrict-filenames --audio-format mp3 '

class RipMusic:
    """A class designed to rip music from YouTube"""
    def __init__(self):
        self.debug = 0
        self.srce = None
        self.dest_dir = DEST + date.today().strftime('%Y_%m_%d')
        if not os.path.exists(self.dest_dir):
            os.makedirs(self.dest_dir)


    @staticmethod
    def error_exit(error_message: str):
        """ exit with an error message"""
        print(error_message)
        print("Exit...")
        sys.exit(1)


    @staticmethod
    def show_help(message=''):
        """Show cmdline interface"""
        message = f'{message}\n {sys.argv[0]} -s <source file>'
        message += '\n<url> <name>'
        print(message)
        sys.exit(2)


    def parse_command_line(self, argv: list):
        """
        Parse cmdline args. It expects '-s <source_file>'. Otherwise it'll exit out with
        a help message.
        """
        function_name = inspect.currentframe().f_code.co_name
        message = f'In {function_name}(), ARGV: {argv}'
        if self.debug > 1:
            print(message)

        try:
            opts, args = getopt.getopt(argv, "hs:a", ["source_file="])
        except getopt.GetoptError:
            error = "cmdline opt error"
            self.show_help(error)

        if len(args) > 0:
            print(f'==>>{args}')
            error = "Unrecognized cmdline args: " + str(argv)
            self.show_help(error)

        if opts:
            for opt, arg in opts:
                if opt == '-h':
                    message = "Showing the correct cmdline usge"
                    self.show_help()
                elif opt in ("-s", "--source_file"):
                    self.srce = arg
                else:
                    error = "cmdline opt error" + str(argv)
                    self.show_help(error)
        else:
            error = "Missing cmdline args"
            self.show_help(error)


    def get_ready(self, url_filename: tuple, thread: dict, result: dict, index: int):
        """
        To spawn two threads - one for ripping the music and the other watches the
        music ripping thread to make sure the ripping is completed.
        :param url_filename: contains the url of a music and the name of the music
        """
        function_name = inspect.currentframe().f_code.co_name
        url = url_filename[0]
        filename = url_filename[1]
        if self.debug:
            print(f'{"="*60}')
            print(f'\nIn {function_name}():\nurl: {url}')
            print(f'index: {index}, thread: {type(thread)}, filename: {filename}')
            print(f'{"="*60}')

        with tempfile.TemporaryDirectory() as temp_dir:
            if self.debug:
                print(f'temp_dir: {temp_dir}')

            thread[index] = {}
            rip = threading.Thread(target=self.rip, args=(url, temp_dir, result, index))
            thread[index][0] = rip
            rip.start()
            rip.join()

            save_file = threading.Thread(target=self.save_file, args=(filename, temp_dir, result, index))
            thread[index][1] = save_file
            save_file.start()
            save_file.join()


    def rip(self, url: str, temp_dir: str, result: dict, index: int):
        """
        To rip a music from youtube by using youtube-dl
        :param url: The url of the music on youtube
        :param temp_dir: a temporary subdirectory that store a ripped music
        """
        function_name = inspect.currentframe().f_code.co_name
        message = f'In {function_name}():\nurl: {url}\ntemp_dir: {temp_dir}'
        if self.debug:
            print(f'{"-"*40}')
            print(message)
            print(f'{"-"*40}')

        cmd = RIP + f' -o "{temp_dir}/%(title)s.%(ext)s" --no-part ' + url
        #subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
        #response = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #try:
        # TODO
        # /home/cyan/mybin/rip_music_thread_in_thread.py:163:16: E0001: multiple exception types \
        #        must be parenthesized (<unknown>, line 163) (syntax-error)
        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as response:
            # Store the return code in rc variable
            return_code = response.wait()
            if index not in result.keys():
                result[index] = {}
            result[index][0] = "Return Code: " + str(return_code)

            # Separate the output and error by communicating with sp variable.
            # This is similar to Tuple where we store two values to two different variables
            out, err = response.communicate()
            if self.debug > 1:
                print(f'output is:\n{out}')
            if err:
                # Note:
                # When run youtube-dl at the prompt, it'll complete gracefully
                # e.g.
                # $ youtube-dl -x --audio-quality 0 -f bestaudio --restrict-filenames \
                #        --audio-format mp3 -o "/tmp/qq/%(title)s.%(ext)s" --no-part \
                #        https://www.youtube.com/watch?v=RmTAUDlcPSk
                # [youtube] RmTAUDlcPSk: Downloading webpage
                # [download] Destination: /tmp/qq/Danny_Chan_-_Official_MV.webm
                # [download] 100% of 3.25MiB in 00:47
                # [ffmpeg] Destination: /tmp/qq/Danny_Chan_-_Official_MV.mp3
                # Deleting original file /tmp/qq/Danny_Chan_-_Official_MV.webm (pass -k to keep)
                #
                # However, if run the same command through subprocess.Popen, it throws an warning:
                # b'WARNING: Cannot update utime of file\nWARNING: Cannot update utime of audio file\n \
                #    WARNING: Unable to remove downloaded original file\n'
                print(f'error is:\n{err}')
        #except subprocess.CalledProcessError, e:
        #    print(f'rip music failed: {e.output}\nfrom URL:\n{url}\n')
            assert return_code == 0, f"\nError!! Return Code is not ZERO: {return_code} {temp_dir}\nURL: {url}\n"

        time.sleep(2)
        # https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread
        # /home/cyan/practice/python/multi_thread_processing/03_thread_in_thread.py
        #return return_code

    # end of def rip(self, url=None, temp_dir=None):

    def save_file(self, filename: str, temp_dir: str, result: dict, index: int):
        """
        To save a music ripped from youtube into a predefined subdirectory
        :param filename: the music's filename
        :param temp_dir: A temporary subdirectory to store a music put by method rip()
        """
        function_name = inspect.currentframe().f_code.co_name
        message = f'In {function_name}():\nfilename: {filename}\ntemp_dir: {temp_dir}'
        if self.debug:
            print(f'{"-"*40}')
            print(message)
            print(f'{"-"*40}')

        mp3_file2look = f"{temp_dir}/*.mp3"
        mp3_files = glob.glob(mp3_file2look)
        j = 0
        while len(mp3_files) != 1 and j < 150:
            time.sleep(2)
            mp3_files = glob.glob(mp3_file2look)
            if len(mp3_files) != 1:
                pass
            else:
                print(f'###===--->>>j = {j}, Length: {len(mp3_files)}, mp3_files: {mp3_files}')
            j += 1
        time.sleep(2)

        try:
            assert len(mp3_files) == 1
            cmd = f"mv {mp3_files[0]} {filename}"
            if index not in result.keys():
                result[index] = {}
            result[index][1] = "File Name: " + filename
            os.system(cmd)
            time.sleep(1)
        except AssertionError:
            print(f"Warning!! In {temp_dir}, mp3_files length: {len(mp3_files)} is NOT one!!")
            return


    def prepare(self) -> dict:
        """
        To read a source file that contains all the music names and the corresponding URLs
        and group them in a dictionary
        :return: url_name_dict:
            keys: URLs
            values: Music names
        """
        function_name = inspect.currentframe().f_code.co_name
        if self.debug:
            print(f'In {function_name}()')

        url_name_dict = {}
        with open(self.srce, "r", encoding="utf8") as file_handle:
            for line in file_handle.readlines():
                line = line.strip()
                if len(line) == 0:
                    continue
                url_name = line.split()
                url = url_name[0]
                name = self.dest_dir + '/' + url_name[1] + '.mp3'
                if os.path.isfile(name):
                    print(f'File exists: {name}')
                    continue
                url_name_dict[url] = name
            # end of for line in file_handle.readlines():
        return url_name_dict
    # end of def prepare(self):

    def summary(self, thread: dict, result: dict):
        """ Show summary"""
        if self.debug:
            for contents in [thread, result]:
                for i in sorted(contents.keys()):
                    for j in sorted(contents[i].keys()):
                        print(f'{i}, {j}, {contents[i][j]}')

        mp3_file2look = f"{self.dest_dir}/*.mp3"
        mp3_files = glob.glob(mp3_file2look)
        if mp3_files:
            mp3_files_count = len(mp3_files)
            for i, filename in enumerate(mp3_files, start=1):
                zeros = ""
                if len(str(i)) < len(str(mp3_files_count)):
                    zeros = "0"*(len(str(mp3_files_count)) - len(str(i)))
                print(f'{zeros}{i}, {filename}')


def main():
    """
    Main method - spawns mutilple threads to rip music concurrently
    """
    start = time.time()
    function_name = inspect.currentframe().f_code.co_name
    obj = RipMusic()
    obj.parse_command_line(sys.argv[1:])
    print(f'\nIn {function_name}(), obj.srce: {obj.srce}')
    url_name = obj.prepare()

    if len(url_name) == 0:
        sys.exit(0)

    thread = defaultdict(dict)
    result = defaultdict(dict)
    # Ref: https://stackoverflow.com/questions/15143837/how-to-multi-thread-an-operation-within-a-loop-in-python
    # Also in OneNote
    pool = Pool(len(url_name))
    index = 1
    for url, filename in url_name.items():
        #pool.apply_async(obj.get_ready, args=([url, filename], thread, index))
        pool.apply_async(obj.get_ready, args=([url, filename], thread, result, index))
        index += 1

    pool.close()
    pool.join()

    obj.summary(thread, result)

    print(f'\nTotal run time: {round((time.time() - start), 3)}\n')
    sys.exit(0)

if __name__ == "__main__":
    main()
