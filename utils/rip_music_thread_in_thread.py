#! /usr/bin/python3
"""
A standalone tool to parse a full patient test's serial console outputs
youtube-dl --extract-audio --audio-format mp3 -o "%(title)s.%(ext)s" http://www.youtube.com/watch?v=rtOvBOTyX00o
youtube-dl -x --audio-quality 0 -f bestaudio --restrict-filenames --audio-format \
        mp3 -o "/tmp/qq/%(title)s.%(ext)s" --no-part https://www.youtube.com/watch?v=6QORyIWN7JI

As of today, 02/20/2023, downloaded yt-dlp using cmd:
-----------------------------------------------------------------------------------
[aquarius] mybin 176 => sudo snap install yt-dlp
yt-dlp a9d069f5b from Graham Morrison (morrisong) installed
[aquarius] mybin 177 => which yt-dlp
/snap/bin/yt-dlp
[aquarius] mybin 178 => yt-dlp --version
2022.11.11

[aquarius] tmp 350 => yt-dlp -U
Latest version: 2023.02.17, Current version: 2022.11.11
ERROR: You installed yt-dlp with a package manager or setup.py; Use that to update

-----------------------------------------------------------------------------------

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

FILEFORMAT = ['mp3', 'mp4']
DEST = '/home/cyan/Music/dest/'
DEST = '/tmp/'
#RIP = 'youtube-dl -x --audio-quality 0 -f bestaudio --restrict-filenames --audio-format mp3 '
#RIPV = 'youtube-dl --recode-video mp4'
RIP = 'yt-dlp -x --audio-quality 0 -f bestaudio --restrict-filenames --audio-format mp3 '
RIPV = 'yt-dlp --recode-video mp4'
FORMAT_RIP = {
    'mp3': RIP,
    'mp4': RIPV
}
# When '-k' is used, the webm files is kept
#RIP = 'youtube-dl -k -x --audio-quality 0 -f bestaudio --restrict-filenames --audio-format mp3 '

class RipMusic:
    """A class designed to rip music from YouTube"""
    def __init__(self):
        self.debug = 0
        self.file_format = 'mp3'
        self.rip_command = RIP
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
        message = f'{message}\n {sys.argv[0]} -s <source file> [-d <debug level>] [-f <file format>]'
        message += f'\nAcceptable file formats: {FILEFORMAT}'
        #message += '\n<url> <name>'
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
            opts, args = getopt.getopt(argv, "hs:d:f:", ["source_file="])
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
                elif opt == '-d':
                    try:
                        if isinstance(int(arg), int):
                            self.debug = int(arg)
                            print(f'debug level: {self.debug}')
                    except ValueError as e:
                        error = f"{e}\nSpecify a debug level: {str(argv)}"
                        self.show_help(error)
                elif opt in ("-s", "--source_file"):
                    if os.path.isfile(arg):
                        self.srce = arg
                    else:
                        error = f"Source file '{arg}' does not exist: {str(argv)}"
                        self.show_help(error)
                elif opt == '-f':
                    if arg not in FILEFORMAT:
                        error = f"Illegal file format '{arg}' given at the cmdline: {str(argv)}"
                        self.show_help(error)
                    self.file_format = arg
                    self.rip_command = RIPV
                else:
                    error = "cmdline opt error" + str(argv)
                    self.show_help(error)
        else:
            error = "Missing cmdline args"
            self.show_help(error)


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

        #cmd = RIP + f' -o "{temp_dir}/%(title)s.%(ext)s" --no-part ' + url
        cmd = self.rip_command + f' -o "{temp_dir}/%(title)s.%(ext)s" --no-part ' + url
        print(f"\n\nCMD:\n{cmd}\n\n")
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
            assert return_code == 0, f"\nError!! Return Code is not ZERO: {return_code} {temp_dir}\nURL: {url}\n"

        time.sleep(2)
        # https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread
        # /home/cyan/practice/python/multi_thread_processing/03_thread_in_thread.py
        #return return_code


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

        if self.file_format == 'mp3':
            mp_file2look = f"{temp_dir}/*.mp3"
            # wait_time * sleep_time = 300 sec = 5 min
            wait_time = 150
            sleep_time = 2
        elif self.file_format == 'mp4':
            mp_file2look = f"{temp_dir}/*.mp4"
            # wait_time * sleep_time = 1800 sec = 30 min
            wait_time = 180
            sleep_time = 10

        mp_files = glob.glob(mp_file2look)
        j = 0
        while len(mp_files) != 1 and j < 150:
            time.sleep(2)
            mp_files = glob.glob(mp_file2look)
            if len(mp_files) != 1:
                pass
            else:
                print(f'###===--->>>j = {j}, Length: {len(mp_files)}, mp_files: {mp_files}')
            j += 1
        time.sleep(2)

        try:
            assert len(mp_files) == 1
            cmd = f"mv {mp_files[0]} {filename}"
            if index not in result.keys():
                result[index] = {}
            result[index][1] = "File Name: " + filename
            os.system(cmd)
            time.sleep(1)
        except AssertionError:
            print(f"Warning!! In {temp_dir}, mp_files length: {len(mp_files)} is NOT one!!")
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
                if self.file_format == 'mp3':
                    name = self.dest_dir + '/' + url_name[1] + '.mp3'
                elif self.file_format == 'mp4':
                    name = self.dest_dir + '/' + url_name[1] + '.mp4'

                if os.path.isfile(name):
                    print(f'File exists: {name}')
                    continue
                url_name_dict[url] = name

        return url_name_dict


    def summary(self, thread: dict, result: dict):
        """ Show summary"""
        if self.debug:
            for contents in [thread, result]:
                for i in sorted(contents.keys()):
                    for j in sorted(contents[i].keys()):
                        print(f'{i}, {j}, {contents[i][j]}')


        if self.file_format == 'mp3':
            mp_file2look = f"{self.dest_dir}/*.mp3"
        elif self.file_format == 'mp4':
            mp_file2look = f"{self.dest_dir}/*.mp4"
        #mp_file2look = f"{self.dest_dir}/*.mp3"
        mp_files = glob.glob(mp_file2look)
        if mp_files:
            mp_files_count = len(mp_files)
            for i, filename in enumerate(mp_files, start=1):
                zeros = ""
                if len(str(i)) < len(str(mp_files_count)):
                    zeros = "0"*(len(str(mp_files_count)) - len(str(i)))
                print(f'{zeros}{i}, {filename}')


    def get_ready(self, url_filename: tuple, base_info: tuple):
        """
        To spawn two threads - one for ripping the music and the other watches the
        music ripping thread to make sure the ripping is completed.
        :param url_filename: contains the url of a music and the name of the music
        """
        start = time.time()
        function_name = inspect.currentframe().f_code.co_name
        url = url_filename[0]
        filename = url_filename[1]
        thread = base_info[0]
        result = base_info[1]
        duration = base_info[2]
        index = base_info[3]
        if self.debug:
            print(f'\n{"="*60}')
            print(f'In {function_name}()')
            print(f'index: {index}, thread: {type(thread)}, filename: {filename}, url: {url}')
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

        print(f'In {function_name}()')
        print(f'Total run time: {round((time.time() - start), 3)}')
        duration[index] = round((time.time() - start), 3)


def main():
    """
    Main method - spawns mutilple threads to rip music concurrently
    """
    start = time.time()
    function_name = inspect.currentframe().f_code.co_name
    obj = RipMusic()
    obj.parse_command_line(sys.argv[1:])
    print(f'In {function_name}(), obj.srce: {obj.srce}, File Format: {obj.file_format}')
    print(f'youtube-dl command: {obj.rip_command}')
    #print(f'{obj.file_format}: {FORMAT_RIP[obj.file_format]}')
    url_name = obj.prepare()

    if len(url_name) == 0:
        sys.exit(0)

    thread = defaultdict(dict)
    result = defaultdict(dict)
    duration = {}
    # Ref: https://stackoverflow.com/questions/15143837/how-to-multi-thread-an-operation-within-a-loop-in-python
    # Also in OneNote
    pool = Pool(len(url_name))
    index = 1
    for url, filename in url_name.items():
        pool.apply_async(obj.get_ready, args=([url, filename], [thread,result,duration,index]))
        index += 1

    pool.close()
    pool.join()

    obj.summary(thread, result)

    print(f'Total run time: {round((time.time() - start), 3)}, Sum: {round(sum(duration.values()), 3)}')
    sys.exit(0)

if __name__ == "__main__":
    main()
