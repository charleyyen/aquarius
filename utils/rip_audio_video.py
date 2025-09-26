#! /usr/bin/python3
"""
A standalone tool to download audio or video from URLs using yt-dlp.
This version features robust source file parsing and a custom directory directive.
"""

import getopt
import inspect
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import date, datetime
from multiprocessing.pool import ThreadPool as Pool
from pathlib import Path

# --- Configuration ---
FILEFORMAT = ['mp3', 'mp4']
DEST_BASE = Path.home() / 'Music' / 'dest'

# yt-dlp command templates
RIP_AUDIO_CMD = 'yt-dlp -x --audio-quality 0 -f bestaudio --restrict-filenames --audio-format mp3'
RIP_VIDEO_CMD = 'yt-dlp -f bestvideo+bestaudio/best --merge-output-format mp4'

FORMAT_RIP_CMDS = {
    'mp3': RIP_AUDIO_CMD,
    'mp4': RIP_VIDEO_CMD
}
# --- End Configuration ---


class RipMusic:
    """A class designed to rip music from YouTube and other sites."""
    def __init__(self):
        self.debug = 0
        self.file_format = 'mp3'
        self.rip_command = FORMAT_RIP_CMDS['mp3']
        self.srce_file = None
        # The final destination directory defaults to a date-stamped directory.
        # This can be overridden by a 'dir=' directive in the source file.
        self.dest_dir = DEST_BASE / date.today().strftime('%Y_%m_%d')

    @staticmethod
    def error_exit(error_message: str):
        """Exit with an error message."""
        print(f"\nERROR: {error_message}")
        print("Exiting...")
        sys.exit(1)

    @staticmethod
    def show_help(message=''):
        """Show command-line interface help."""
        if message:
            print(f"Error: {message}\n")
        usage = f"Usage: {sys.argv[0]} -s <source_file> [-f <format>] [-d <debug_level>]"
        usage += f"\n\n  -s, --source_file  : Required. File containing URLs and names."
        usage += f"\n  -f, --format       : Optional. 'mp3' (default) or 'mp4'."
        usage += f"\n  -d, --debug        : Optional. Debugging level (e.g., 1)."
        usage += f"\n  -h, --help         : Show this help message."
        print(usage)
        sys.exit(2)

    def parse_command_line(self, argv: list):
        """Parse command-line arguments."""
        try:
            opts, args = getopt.getopt(argv, "hs:f:d:", ["help", "source_file=", "format="])
        except getopt.GetoptError as e:
            self.show_help(str(e))

        if not opts:
            self.show_help("No options provided.")

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                self.show_help()
            elif opt in ("-s", "--source_file"):
                source_path = Path(arg)
                if source_path.is_file():
                    self.srce_file = source_path
                else:
                    self.error_exit(f"Source file '{arg}' does not exist.")
            elif opt in ("-f", "--format"):
                if arg in FILEFORMAT:
                    self.file_format = arg
                    self.rip_command = FORMAT_RIP_CMDS[arg]
                else:
                    self.show_help(f"Invalid format '{arg}'. Accepted formats: {FILEFORMAT}")
            elif opt == '-d':
                self.debug = int(arg)

        if self.srce_file is None:
            self.show_help("The source file (-s) is a required argument.")

    def prepare(self) -> dict:
        """
        Reads the source file, checks for a custom 'dir=' directive on the first valid line,
        sets the destination directory, and returns a dictionary of URLs and filenames.
        """
        if self.debug:
            print(f"Reading source file: {self.srce_file}")

        with open(self.srce_file, "r", encoding="utf8") as f:
            lines = f.readlines()

        # Filter out empty lines and comments first.
        valid_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                valid_lines.append(line)

        if not valid_lines:
            return {}

        # --- ENHANCEMENT: Check ONLY the first valid line for the 'dir=' directive ---
        first_line = valid_lines[0]
        parts = first_line.split('=', 1)

        # Robustly check for 'dir = value' with spaces and case-insensitivity
        if len(parts) == 2 and parts[0].strip().lower() == 'dir':
            custom_dir_name = parts[1].strip()
            if custom_dir_name: # Ensure the value is not empty
                self.dest_dir = DEST_BASE / custom_dir_name
                # Remove the directive line so it's not processed as a URL
                valid_lines.pop(0)
        # --- End of Enhancement ---

        # Ensure the final destination directory exists (either custom or default)
        self.dest_dir.mkdir(parents=True, exist_ok=True)

        url_name_dict = {}
        for line in valid_lines:
            # Split by whitespace to get URL and name parts
            parts = line.split()
            if len(parts) < 2:
                continue

            url = parts[0]
            base_name = "_".join(parts[1:])
            dest_path = self.dest_dir / f"{base_name}.{self.file_format}"

            if dest_path.exists():
                print(f'Skipping, file already exists: {dest_path.name}')
                continue
            url_name_dict[url] = dest_path

        return url_name_dict

    def download_and_save(self, url: str, dest_path: Path):
        """
        This is the worker function for the ThreadPool.
        It downloads, converts, and saves a single file.
        """
        start_time = time.time()
        print(f"[{dest_path.name}] Starting download...")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            cmd = self.rip_command + f' -o "{temp_path / "%(title)s.%(ext)s"}" --no-part ' + url
            if self.debug:
                print(f"[{dest_path.name}] Executing command:\n{cmd}")

            try:
                subprocess.run(
                    cmd, shell=True, check=True, capture_output=True, text=True
                )
            except subprocess.CalledProcessError as e:
                print(f"--- ERROR: Failed to download {url} ---")
                print(f"Return Code: {e.returncode}")
                print(f"Stderr:\n{e.stderr.strip()}")
                print("-----------------------------------------")
                return

            extension = f"*.{self.file_format}"
            downloaded_files = list(temp_path.glob(extension))

            if downloaded_files:
                shutil.move(downloaded_files[0], dest_path)
                duration = round(time.time() - start_time, 2)
                print(f"[{dest_path.name}] Finished in {duration}s.")
            else:
                print(f"WARNING: Could not find converted file for {url} in {temp_dir}")

def main():
    """Main method - spawns mutilple threads to rip media concurrently."""
    if not shutil.which("yt-dlp"):
        RipMusic.error_exit("yt-dlp is not installed or not in your PATH.")
    if not shutil.which("ffmpeg"):
        RipMusic.error_exit("ffmpeg is not installed or not in your PATH.")

    start_time = time.time()
    obj = RipMusic()
    obj.parse_command_line(sys.argv[1:])

    # 'prepare' now handles all source file parsing and sets the final destination directory
    url_map = obj.prepare()

    print(f'\nSource file: {obj.srce_file}')
    print(f'Saving to: {obj.dest_dir}')
    print(f'Format: {obj.file_format}')

    if not url_map:
        print("No new files to download.")
        sys.exit(0)

    print(f"\nFound {len(url_map)} new files to download...")

    pool_size = min(len(url_map), 10)
    pool = Pool(pool_size)

    for url, dest_path in url_map.items():
        pool.apply_async(obj.download_and_save, args=(url, dest_path))

    pool.close()
    pool.join()

    total_duration = round(time.time() - start_time, 2)
    print(f"\nBatch completed in {total_duration} seconds.")

    try:
        now = datetime.now()
        timestamp_str = now.strftime("%A, %B %d, %Y at %I:%M %p")
        log_message = f"\n# Above musics are downloaded on {timestamp_str}\n\n"

        with open(obj.srce_file, 'a', encoding='utf-8') as f:
            f.write(log_message)
        print(f"Successfully added completion timestamp to {obj.srce_file.name}")
    except Exception as e:
        print(f"Warning: Could not write timestamp to source file. Error: {e}")

    sys.exit(0)

if __name__ == "__main__":
    main()

