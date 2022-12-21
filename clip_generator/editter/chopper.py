import os
import subprocess

import clip_generator.editter.dirs as dirs
from clip_generator.common_functions import remove_file_extension


def remove_video(dir_input: str, dir_output: str):
    os.system(f"ffmpeg -loglevel error -stats -y -i {dir_input} -vn {dir_output}")

# untested and seems like useless
#def extract_audio(file):
#
#    os.system(f" ffmpeg -i '{file}' -c:a pcm_s24le '{filepath_wo_suffix}.wav'")


def slow_audio(input_audio):
    output_audio = str(remove_file_extension(input_audio)) + "_slowed.mp4"

    slowness = "atempo=0.5,atempo=0.5,atempo=0.5,atempo=0.5,atempo=0.5,atempo=0.5"
    if dirs.get_second() == 3:
        slowness = "atempo=0.5,atempo=0.5,atempo=0.5,atempo=0.5"
    os.system(f'ffmpeg  -loglevel error -stats -y -i {input_audio} -filter:a "{slowness}" -vn {output_audio}')
    return output_audio


# TODO get total audio parts number and set it in a local var
# Input: String: seconds
def cutAudioIntoXSecondsParts(x: str):
    os.system(
        f"ffmpeg -loglevel error -stats -y -i {dirs.dir_audio_clip}  -segment_time 00:00:{x} -f segment -strict -2  -map 0 -c:a aac {dirs.dirAudioParts}S{x}_clip_audio%01d.mp4")


# Input: Int: length of cut audio from the last seconds
def cutLastSecondsAudio(seconds: int, offset_credits=0):
    cutted_seconds = str(
        seconds + offset_credits + dirs.transition_offset)  # Usually the last second is a transition from the clip to credits or it simply loses volume to zero in the span of 1-2 seconds, this could interfere with the comparasons, so it gets left out
    real_seconds = str(seconds)
    os.system(
        f"ffmpeg -loglevel error -stats -y -sseof -{cutted_seconds} -i {dirs.dir_audio_clip} -c copy {dirs.dirAudioParts}temp_last_S{real_seconds}_clip_audio.mp4")
    os.system(# TODO SEEMS Like this only works if its only 3 seconds the cut
        "ffmpeg -loglevel error -stats -y -ss 0 -to 00:00:03 -i " + dirs.dirAudioParts + "temp_last_S" + real_seconds + "_clip_audio.mp4 -c copy " + dirs.dirAudioParts + "last_S" + real_seconds + "_clip_audio.mp4")


def fixAudioParts():
    filenames = next(os.walk(dirs.dirAudioParts), (None, None, []))[2]
    for filename in filenames:
        os.system(
            "ffmpeg -loglevel error -stats -y -ss 00:00:00 -i " + dirs.dirAudioParts + filename + " " + dirs.dirFixedAudioParts + filename)


def chop(input_file, output_file, from_second: str, to_second: str):
    os.system(
        f"ffmpeg -loglevel error -stats -y -ss {from_second} -to {to_second} -i {input_file} {output_file}")


# Given a array, it will make the edits given timestamps
def final_chop(input_file, output_file, time_intervals):
    # Create the select and aselect filters for FFmpeg
    select_filter = "select='"
    aselect_filter = "aselect='"
    for interval in time_intervals:
        start, end = interval
        select_filter += f"between(t,{start},{end})+"
        aselect_filter += f"between(t,{start},{end})+"
    select_filter = select_filter[:-1] + "',setpts=N/FRAME_RATE/TB"
    aselect_filter = aselect_filter[:-1] + "',asetpts=N/SR/TB"

    # Call FFmpeg with the select and aselect filters
    subprocess.run(["ffmpeg", "-i", input_file, "-vf", select_filter, "-af", aselect_filter, output_file])
