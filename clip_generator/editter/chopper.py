import os
import sys

import clip_generator.editter.audio_info as audio_info


dirAudioParts = "clip_generator/editter/audio_parts/"
dirFixedAudioParts = "editter/fixed_audio_parts/"
dir_clip = "../Clips/clip.mkv"
dir_audio_clip = "clip_generator/editter/clip_audio.mp4"

def removeVideo():
	os.system(f"ffmpeg -y -i {dir_clip} -vn {dir_audio_clip}")

# Input: String: seconds in %01d
def cutAudioIntoXSecondsParts(x):
	os.system(f"ffmpeg -y -i {dir_audio_clip}  -segment_time 00:00:{x} -f segment -strict -2  -map 0 -c:a aac {dirAudioParts}S{x}_clip_audio%01d.mp4")

# Input: Int/String: length of cutted audio from the last seconds
def cutLastSecondsAudio(seconds):
	cutted_seconds = str(seconds+1)
	real_seconds = str(seconds)
	os.system("ffmpeg -y -sseof -"+ cutted_seconds +" -i editter/clip_audio.mp4 -c copy "+ dirAudioParts +"temp_last_S"+ real_seconds +"_clip_audio.mp4")
	os.system("ffmpeg -y -ss 0 -to 00:00:03 -i "+ dirAudioParts +"temp_last_S"+ real_seconds +"_clip_audio.mp4 -c copy "+ dirAudioParts +"last_S"+ real_seconds +"_clip_audio.mp4")

def fixAudioParts():
	filenames = next(os.walk(dirAudioParts), (None, None, []))[2]
	for filename in filenames:
		os.system("ffmpeg -y -ss 00:00:00 -i " + dirAudioParts + filename + " " + dirFixedAudioParts + filename)

def chop():
	to_second = audio_info.last_seconds_to_argument_to("../Clips/stream.mkv", audio_info.infosTrim[1][0][1]['pad_post'])
	os.system("ffmpeg -y -ss "+str(audio_info.infosTrim[0][0][1]['pad'])+" -to "+ str(to_second) + " -i ../Clips/stream.mkv ../Clips/trimmed_stream.mkv")
