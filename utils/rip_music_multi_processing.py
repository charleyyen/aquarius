"""
A standalone tool to parse a full patient test's serial console outputs
youtube-dl --extract-audio --audio-format mp3 -o "%(title)s.%(ext)s" http://www.youtube.com/watch?v=rtOvBOTyX00o
youtube-dl -x --audio-quality 0 -f bestaudio --restrict-filenames --audio-format mp3 -o "/tmp/qq/%(title)s.%(ext)s" --no-part https://www.youtube.com/watch?v=6QORyIWN7JI
"""

import getopt
import glob
import inspect
import os
import multiprocessing
import subprocess
import sys
import tempfile
import time

from collections import defaultdict
from datetime import date
from multiprocessing.pool import ThreadPool as Pool

DEST = '/home/cyan/Music/dest/'
DEST = '/tmp/'
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
    def error_exit(error_message):
        """ exit with an error message"""
        print(error_message)
        print("Exit...")
        sys.exit(1)


    @staticmethod
    def show_help(message=''):
        """Show cmdline interface"""
        message = f'{message}\n {sys.argv[0]} -s <source file>'
        message += f'\n<url> <name>'
        print(message)
        sys.exit(2)


    def parse_command_line(self, argv):
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


    def rip(self, url=None, temp_dir=None):
        function_name = inspect.currentframe().f_code.co_name
        message = f'In {function_name}()\nurl: {url}\ntemp_dir: {temp_dir}'
        print(message)
        try:
            assert url and temp_dir
        except AssertionError:
            print("Either url or temp_dir is None. Exit...")
            return

        cmd = RIP + f' -o "{temp_dir.name}/%(title)s.%(ext)s" --no-part ' + url
        print(f'cmd:\n{cmd}')

        #subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
        sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Store the return code in rc variable
        rc=sp.wait()
        assert rc == 0, f"Error!! Return Code is not ZERO: {rc}"
        # Separate the output and error by communicating with sp variable.
        # This is similar to Tuple where we store two values to two different variables
        out,err=sp.communicate()

        print(f'Return Code: {rc}')
        #print(f'output is:\n{out}')
        if err:
            """
            # Note:
            # When run youtube-dl at the prompt, it'll complete gracefully
            # e.g.
            youtube-dl -x --audio-quality 0 -f bestaudio --restrict-filenames --audio-format mp3  -o "/tmp/qq/%(title)s.%(ext)s" --no-part https://www.youtube.com/watch?v=RmTAUDlcPSk
            [youtube] RmTAUDlcPSk: Downloading webpage
            [download] Destination: /tmp/qq/Danny_Chan_-_Official_MV.webm
            [download] 100% of 3.25MiB in 00:47
            [ffmpeg] Destination: /tmp/qq/Danny_Chan_-_Official_MV.mp3
            Deleting original file /tmp/qq/Danny_Chan_-_Official_MV.webm (pass -k to keep)
            #
            # However, if run the same command through subprocess.Popen, it throws an error (warning):
            # b'WARNING: Cannot update utime of file\nWARNING: Cannot update utime of audio file\nWARNING: Unable to remove downloaded original file\n'
            """
            print(f'error is:\n{err}')

        time.sleep(2)

    def rename_ripped_file(self, filename=None, temp_dir=None):
        function_name = inspect.currentframe().f_code.co_name
        message = f'In {function_name}()\nfilename: {filename}\ntemp_dir: {temp_dir}'
        print(message)
        try:
            assert filename and temp_dir
        except AssertionError:
            print("Either temp_dir or filename is None. Exit...")
            return

        time.sleep(3)

        mp3_file2look = f"{temp_dir.name}/*.mp3"
        mp3_files = glob.glob(mp3_file2look)
        print(f'\n\n==-->>Length: {len(mp3_files)}, mp3_files: {mp3_files}')
        j = 0
        while len(mp3_files) != 1 and j < 300:
            time.sleep(2)
            mp3_files = glob.glob(mp3_file2look)
            if len(mp3_files) != 1:
                if j%5 == 0:
                    print(f'j = {j}')
            else:
                print(f'###===--->>>j = {j}, Length: {len(mp3_files)}, mp3_files: {mp3_files}')
            j += 1
        time.sleep(2)

        try:
            assert len(mp3_files) == 1
            cmd = f"mv {mp3_files[0]} {filename}"
            os.system(cmd)
            time.sleep(1)
            temp_dir.cleanup()
        except AssertionError:
            print(f"Warning!! In {temp_dir.name}, mp3_files length: {len(mp3_files)} is NOT one!!")
            return False


    def prepare(self):
        function_name = inspect.currentframe().f_code.co_name
        original_file_size = 0
        file_size = 1
        file_handle = open(self.srce, "r")
        url_name_dict = {}
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
            else:
                url_name_dict[url] = name

        return url_name_dict


def main():
    start = time.time()
    function_name = inspect.currentframe().f_code.co_name
    obj = RipMusic()
    obj.parse_command_line(sys.argv[1:])
    print(f'In {function_name}(), obj.srce: {obj.srce}')
    url_name = obj.prepare()
    for url, filename in url_name.items():
        temp_dir = tempfile.TemporaryDirectory()
        result = []
        flag = True
        with multiprocessing.Pool() as mpool:
            result.append(mpool.apply_async(obj.rip, (url,temp_dir)))
            result.append(mpool.apply_async(obj.rename_ripped_file, (filename,temp_dir)))

            for r in result:
                r.wait()

        if flag:
            temp_dir.cleanup()
        else:
            print(f'Manually check what is in "{temp_dir.name}"')
        print(f'{"*"*60}')

    print(f'Total run time: {round((time.time() - start), 3)}')
    sys.exit(0)

if __name__ == "__main__":
    main()

