import math
import subprocess
import difflib
import os
from PIL import Image, ImageDraw

from pathlib import Path
from shutil import rmtree

import clip_generator.editter.dirs as dirs

# None of them has tests

def getDuration(filename):
    duration = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
         filename], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return float(duration)


def removeAll(folder_path):
    for path in Path(folder_path).glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path, ignore_errors=True)

    os.makedirs(dirs.dirAudioParts, exist_ok=True)
    os.makedirs(dirs.dirFixedAudioParts, exist_ok=True)


def checkTwoFilesAreTheSame(filename1, filename2):
    IsSame = True
    with open(filename1) as file_1:
        file_1_text = file_1.readlines()

    with open(filename2) as file_2:
        file_2_text = file_2.readlines()

    for line in difflib.unified_diff(
            file_1_text, file_2_text, fromfile=filename1,
            tofile=filename2, lineterm=''):
        print(line)
        if line is not None:
            IsSame = False
    return IsSame


def check_two_large_files_are_equal(filepath1, filepath2):
    if os.path.getsize(filepath1) == os.path.getsize(filepath2):
        return True
    return False


def remove_file_extension(file):
    filepath = Path(file)
    return filepath.with_suffix('')


def calculate_part_audio_files(total_duration, part_duration):
    return math.ceil(total_duration / part_duration)
