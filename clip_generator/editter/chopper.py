import os
import sys

from clip_generator.editter.dirs import dir_clip
from clip_generator.editter.dirs import dir_audio_clip
from clip_generator.editter.dirs import dirAudioParts
from clip_generator.editter.dirs import dirFixedAudioParts
from clip_generator.editter.dirs import dir_stream
from clip_generator.editter.dirs import dir_trimmed_stream

def removeVideo():
	os.system(f"ffmpeg -loglevel error -stats -y -i {dir_clip} -vn {dir_audio_clip}")

# Input: String: seconds in %01d
def cutAudioIntoXSecondsParts(x):
	os.system(f"ffmpeg -loglevel error -stats -y -i {dir_audio_clip}  -segment_time 00:00:{x} -f segment -strict -2  -map 0 -c:a aac {dirAudioParts}S{x}_clip_audio%01d.mp4")

# Input: Int: length of cutted audio from the last seconds
def cutLastSecondsAudio(seconds):
	cutted_seconds = str(seconds+1)
	real_seconds = str(seconds)
	os.system(f"ffmpeg -loglevel error -stats -y -sseof -{cutted_seconds} -i {dir_audio_clip} -c copy {dirAudioParts}temp_last_S{real_seconds}_clip_audio.mp4")
	os.system("ffmpeg -loglevel error -stats -y -ss 0 -to 00:00:03 -i "+ dirAudioParts +"temp_last_S"+ real_seconds +"_clip_audio.mp4 -c copy "+ dirAudioParts +"last_S"+ real_seconds +"_clip_audio.mp4")

def fixAudioParts():
	filenames = next(os.walk(dirAudioParts), (None, None, []))[2]
	for filename in filenames:
		os.system("ffmpeg -loglevel error -stats -y -ss 00:00:00 -i " + dirAudioParts + filename + " " + dirFixedAudioParts + filename)

def chop(from_second, to_second):
	os.system(f"ffmpeg -loglevel error -stats -y -ss {from_second} -to {to_second} -i {dir_stream} {dir_trimmed_stream}")
