import speech_recognition as sr
from os import path
from pydub import AudioSegment
import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf 
import os 
import pdb

def transcribe_audio(f):
	if f.endswith(".mp3") or f.endswith(".MP3"): 
		sound = AudioSegment.from_mp3(f)
		#root.destroy()
		#filenm = input("What file would you like to export as(wav)? ")
		sound.export("transcript.wav", format="wav")
		AUDIO_FILE = "transcript.wav"
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)
		transcription = r.recognize_google(audio) #class 'str'
		return transcription
	elif f.endswith(".wav") or f.endswith(".WAV"): 
		AUDIO_FILE = f
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)
		transcription = r.recognize_google(audio) #class 'str'
		return transcription
	elif f.endswith('.flac'):
		sound = AudioSegment.from_file(f, "flac")
		sound.export("transcript.wav", format="wav")
		AUDIO_FILE = "transcript.wav"
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
			audio = r.record(source)
		transcription = r.recognize_google(audio) #class 'str'
		return transcription
	elif f.endswith('.ogg'):
		os.system("ffmpeg -i " + f + " output.wav")
		f= "output.wav"
		AUDIO_FILE = f
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)
		transcription = r.recognize_google(audio) #class 'str'
		return transcription
	elif f.endswith('.m4a'):
		sound = AudioSegment.from_file(f, "m4a")
		sound.export("transcript.wav", format="wav")
		AUDIO_FILE = "transcript.wav"
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)
		transcription = r.recognize_google(audio) #class 'str'
		return transcription

def transcribe_audio_french(f):
	if f.endswith(".mp3"):
		sound = AudioSegment.from_mp3(f)
		sound.export("transcript.wav", format="wav")
		AUDIO_FILE = "transcript.wav"
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
			audio = r.record(source)
		transcription = r.recognize_google(audio, language="fr-FR") #class 'str'
		return transcription
	elif f.endswith(".wav"): 
		AUDIO_FILE = f
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
			audio = r.record(source)
		transcription = r.recognize_google(audio, language="fr-FR") #class 'str'
		return transcription
	elif f.endswith('.flac'):
		sound = AudioSegment.from_file(f, "flac")
		sound.export("transcript.wav", format="wav")
		AUDIO_FILE = "transcript.wav"
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
			audio = r.record(source)
		transcription = r.recognize_google(audio, language="fr-FR") #class 'str'
		return transcription
	elif f.endswith('.ogg'):
		os.system("ffmpeg -i " + f + " output.wav")
		f= "output.wav"
		AUDIO_FILE = f
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)
		transcription = r.recognize_google(audio) #class 'str'
		return transcription
	elif f.endswith('.m4a'):
		sound = AudioSegment.from_file(f, "m4a")
		sound.export("transcript.wav", format="wav")
		AUDIO_FILE = "transcript.wav"
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)
		transcription = r.recognize_google(audio, language="fr-FR") #class 'str'
		return transcription

def transcribe_audio_chinese(f):
	if ".mp3" in f: 
		sound = AudioSegment.from_mp3(f)
		#root.destroy()
		#filenm = input("What file would you like to export as(wav)? ")
		sound.export("transcript.wav", format="wav")

		AUDIO_FILE = "transcript.wav"

		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)

		#print("Transcription: " + r.recognize_google(audio))
		transcription = r.recognize_google(audio, language="zh-CN") #class 'str'
		return transcription
	elif ".wav" in f: 
		AUDIO_FILE = f

		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)
		transcription = r.recognize_google(audio, language="zh-CN") #class 'str'
		return transcription
	elif f.endswith('.flac'):
		sound = AudioSegment.from_file(f, "flac")
		sound.export("transcript.wav", format="wav")
		AUDIO_FILE = "transcript.wav"
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)
		transcription = r.recognize_google(audio, language="zh-CN") #class 'str'
		return transcription
	elif f.endswith('.ogg'):
		os.system("ffmpeg -i " + f + " output.wav")
		f= "output.wav"
		AUDIO_FILE = f
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)
		transcription = r.recognize_google(audio) #class 'str'
		return transcription
	elif f.endswith('.m4a'):
		sound = AudioSegment.from_file(f, "m4a")
		sound.export("transcript.wav", format="wav")
		AUDIO_FILE = "transcript.wav"
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)
		transcription = r.recognize_google(audio, language="zh-CN") #class 'str'
		return transcription

def transcribe_audio_naspanish(f):
	if ".mp3" in f: 
		sound = AudioSegment.from_mp3(f)
		sound.export("transcript.wav", format="wav")
		AUDIO_FILE = "transcript.wav"
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)
		#print("Transcription: " + r.recognize_google(audio))
		transcription = r.recognize_google(audio, language="es-MX") #class 'str'
		return transcription
	elif ".wav" in f: 
		AUDIO_FILE = f
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)
		transcription = r.recognize_google(audio, language="es-MX") #class 'str'
		return transcription
	elif f.endswith('.flac'):
		sound = AudioSegment.from_file(f, "flac")
		sound.export("transcript.wav", format="wav")
		AUDIO_FILE = "transcript.wav"
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)
		transcription = r.recognize_google(audio, language="es-MX") #class 'str'
		return transcription
	elif f.endswith('.ogg'):
		os.system("ffmpeg -i " + f + " output.wav")
		f= "output.wav"
		AUDIO_FILE = f
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)
		transcription = r.recognize_google(audio) #class 'str'
		return transcription
	elif f.endswith('.m4a'):
		sound = AudioSegment.from_file(f, "m4a")
		sound.export("transcript.wav", format="wav")
		AUDIO_FILE = "transcript.wav"
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)
		transcription = r.recognize_google(audio, language="es-MX") #class 'str'
		return transcription
			
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/catherineng/Downloads/My Project 52130-da00a565db68.json"
import pdb


import subprocess
import shlex
import json

def get_duration_channels(filename):
	#cmd = 'ffprobe -show_entries format=duration -v quiet -of csv="p=0"'
	cmd = 'ffprobe -show_entries stream=channels -select_streams a:0 -of compact=p=0:nk=1 -v 0'
	args = shlex.split(cmd)
	args.append(filename)
	# run the ffprobe process, decode stdout into utf-8 & convert to JSON
	ffprobe_output = subprocess.check_output(args).decode('utf-8')

	ffprobe_output = json.loads(ffprobe_output)

	return ffprobe_output

def get_duration(filename):
	#cmd = 'ffprobe -show_entries format=duration -v quiet -of csv="p=0"'
	#cmd = 'ffprobe -show_entries stream=channels -select_streams a:0 -of compact=p=0:nk=1 -v 0'
	cmd = 'ffprobe -select_streams a -show_entries stream=sample_rate -of compact=p=0:nk=1 -v 0' #static/uploaded_files/output7.wav
	args = shlex.split(cmd)
	args.append(filename)
	# run the ffprobe process, decode stdout into utf-8 & convert to JSON
	ffprobe_output = subprocess.check_output(args).decode('utf-8')

	ffprobe_output = json.loads(ffprobe_output)

	return ffprobe_output

def transcribe_google_punct(path): 
	from google.cloud import speech
	client = speech.SpeechClient()

	#path = "/Users/catherineng/Desktop/Python_Projects/huntercodefest/app/static/uploaded_files/transcript.wav"
	import io
	with io.open(path, 'rb') as audio_file:
		content = audio_file.read()
	#audio = {"uri": storage_uri}
	
	audio = speech.types.RecognitionAudio(content=content)
	config = speech.types.RecognitionConfig(
		encoding=speech.enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
		#sample_rate_hertz=8000,
		#sample_rate_hertz=22050,
		sample_rate_hertz= get_duration(path), 
		audio_channel_count = get_duration_channels(path), 
		language_code='en-US',
		# Enable automatic punctuation
		enable_automatic_punctuation=True)

	response = client.recognize(config, audio)

	for i, result in enumerate(response.results):
		alternative = result.alternatives[0]
		tuple = alternative.transcript
		#print('-' * 20)
		#print('First alternative of result {}'.format(i))
		#print('Transcript: {}'.format(alternative.transcript))
		return tuple
