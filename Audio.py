'''import speech_recognition as sr
from os import path
from pydub import AudioSegment
import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf 

from tkinter import filedialog
from tkinter import *

def quit():
	root.destroy()
root = Tk()
root.withdraw()
file =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Audio files",".mp3"),("all files","*.*")))
print(file)
#if file = None:
#    data = file.read()
#    file.close()

#1. UPLOAD FILE
def transcribe_audio():
	sound = AudioSegment.from_mp3(file)
	root.destroy()
	filenm = input("What file would you like to export as(wav)? ")
	sound.export(filenm, format="wav")

	AUDIO_FILE = filenm

	r = sr.Recognizer()
	with sr.AudioFile(AUDIO_FILE) as source:
	audio = r.record(source)

	#print("Transcription: " + r.recognize_google(audio))
	transcription = r.recognize_google(audio) #class 'str'
	print("Transcription: " + transcription)

	def word_counts(str): 
		counts = dict()
		words = str.split()

		for word in words:
			if word in counts:
				counts[word] += 1
			else:
				counts[word] = 1
		return counts

	data = word_counts(transcription.lower())
	print(data)

	import matplotlib.pyplot as plt

	#keys = data.keys()
	#vals = data.values()

	#Make Bar Graph
	plt.bar(*zip(*data.items()), label = "Word counts")
	plt.xticks(rotation='vertical')
	plt.xlabel('Words')
	plt.tight_layout() 
	plt.savefig('bar.png')


	import numpy as np
	import pandas as pd
	from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
	from PIL import Image
	from os import path
	import matplotlib.pyplot as plt

	text = (transcription)

	american_flag = np.array(Image.open("american_flag.png"))

	wordcloud = WordCloud( width = 480, height = 480, 
					background_color ='white', 
					max_words = 20,
					mask = american_flag,
					#stopwords = stopwords, 
					min_font_size = 10
					).generate(text) 
	# plot the WordCloud image                        
	#plt.figure(figsize = (8, 8), facecolor = None) 
	# plt.figure()
	plt.imshow(wordcloud, interpolation='bilinear') 
	plt.axis("off") 
	plt.margins(x=0, y=0)
	#plt.tight_layout(pad = 0) 
	wordcloud.to_file("wordCloud.png")  
'''
'''
#1. RECORD AND SAVE AUDIO FILE
import pydub

fs = 44100  # Sample rate
seconds = 3  # Duration of recording

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
print("Say Something!")
sd.wait()  # Wait until recording is finished
sd.play(myrecording, fs)
sd.stop()
#recognizer_instance.adjust_for_ambient_noise(source, duration = 1)
import wavio

filename = input("What will you write this audio to? ")
wavio.write(filename, myrecording, fs, sampwidth=2)

#wavio.write("output.wav", myrecording, fs, sampwidth=2)

AUDIO_FILE2 = filename
#AUDIO_FILE2 = "output.wav"

r = sr.Recognizer()
#r.energy_threshold = 4000
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE2) as source:
   audio = r.record(source)
   print("Transcription: " + r.recognize_google(audio))
transcription = r.recognize_google(audio) #class 'str'

def word_counts(str): 
	counts = dict()
	words = str.split()

	for word in words:
		if word in counts:
			counts[word] += 1
		else:
			counts[word] = 1
	return counts

data = word_counts(transcription.lower())
print(data)

#Make Bar Graph
plt.bar(*zip(*data.items()), label = "Word counts")
plt.xticks(rotation='vertical')
plt.xlabel('Words')
plt.tight_layout() 
plt.savefig('record_bar.png')

import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt

df = pd.DataFrame.from_dict(data, orient='index')
print(df)

text = (transcription)
wordcloud = WordCloud(width = 800, height = 800, margin=0,
				background_color ='white', 
				max_words = 100,
				#stopwords = stopwords, 
				#min_font_size = 10
				).generate(transcription) 
# plot the WordCloud image                        
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud, interpolation='bilinear') 
plt.axis("off") 
plt.margins(x=0, y=0)
#plt.tight_layout(pad = 0) 
  
plt.show() 
#recognizer_instance.dynamic_energy_threshold = True # type: bool

#with sr.Microphone() as source:
#    r.adjust_for_ambient_noise(source) 
#    print("Say something!")
#    audio = r.listen(source)


# with sr.WavFile("output.wav") as source:              # use "test.wav" as the audio source
#     audio = r.record(source)                        # extract audio data from the file

# try:
#     list = r.recognize(audio,True)                  # generate a list of possible transcriptions
#     print("Possible transcriptions:")
#     for prediction in list:
#         print(" " + prediction["text"] + " (" + str(prediction["confidence"]*100) + "%)")
# except LookupError:                                 # speech is unintelligible
#     print("Could not understand audio")
'''

'''
import tkinter as tk

def show_entry_fields():
	print("What file would you like to upload?: %s" % (e1.get())

master = tk.Tk()
tk.Label(master, text="What file would you like to upload?(mp3, flac, etc) ").grid(row=0)
#tk.Label(master, text="Last Name").grid(row=1)

e1 = tk.Entry(master)
#e2 = tk.Entry(master)

e1.grid(row=0, column=1)
#e2.grid(row=1, column=1)

tk.Button(master, 
		  text='Quit', 
		  command=master.quit).grid(row=3, 
									column=0, 
									sticky=tk.W, 
									pady=4)
tk.Button(master, 
		  text='Show', command=show_entry_fields).grid(row=3, 
													   column=1, 
													   sticky=tk.W, 
													   pady=4)

master.mainloop()  
'''
'''import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/catherineng/Downloads/My Project 52130-da00a565db68.json"

import speech_recognition as sr
from os import path
from pydub import AudioSegment
import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf 
import os

def transcribe_google_punct(path): 
	from google.cloud import speech
	client = speech.SpeechClient()
	path = "/Users/catherineng/Desktop/Python_Projects/huntercodefest/app/static/uploaded_files/transcript.mp3"
	import io

	with io.open(path, 'rb') as audio_file:
		content = audio_file.read()
	#audio = {"uri": storage_uri}


	audio = speech.types.RecognitionAudio(content=content)
	config = speech.types.RecognitionConfig(
		encoding=speech.enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
		sample_rate_hertz=8000,
		language_code='en-US',
		# Enable automatic punctuation
		enable_automatic_punctuation=True)

	response = client.recognize(config, audio)

	for i, result in enumerate(response.results):
		alternative = result.alternatives[0]
		tuple = (i, alternative.transcript)
		#print('-' * 20)
		#print('First alternative of result {}'.format(i))
		#print('Transcript: {}'.format(alternative.transcript))
		return tuple

print(transcribe_google_punct(path))'''

def length_wav(fname): #finding the length of audio file
	import wave
	import contextlib
	with contextlib.closing(wave.open(fname,'r')) as f:
		frames = f.getnframes()
		rate = f.getframerate()
		duration = frames / float(rate)
	return duration

#print(length_wav("/Users/catherineng/Desktop/Python_Projects/huntercodefest/app/output.wav"))

import speech_recognition as sr
from os import path
from pydub import AudioSegment
import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf 
import os

def transcribe_audio(f):
	if f.endswith('.ogg'):
		sound = AudioSegment.from_ogg(f)
		sound.export("transcript.wav", format="wav")
		AUDIO_FILE = "transcript.wav"
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
			audio = r.record(source)
		transcription = r.recognize_google(audio) #class 'str'
		return transcription

#print(transcribe_audio("/Users/catherineng/Downloads/Example.ogg"))

def length_wav(fname): #finding the length of audio file
	import wave
	import contextlib
	if fname.endswith(".wav") or fname.endswith(".WAV"):
		with contextlib.closing(wave.open(fname,'r')) as f:
			frames = f.getnframes()
			rate = f.getframerate()
			duration = frames / float(rate)
		return duration
	if fname.endswith(".mp3") or fname.endswith(".MP3"):
		from mutagen.mp3 import MP3
		audio = MP3(fname)
		return audio.info.length 
	if fname.endswith(".flac"):
		from mutagen.flac import FLAC
		audio = FLAC(fname)
		return audio.info.length
	if fname.endswith(".ogg"):
		import mutagen
		audio = mutagen.File(fname)
		#maim =  
		if audio is None: 
			var = os.system("ffmpeg -i /Users/catherineng/Downloads/0aeaedfc-b0ee-4ad1-a6b7-85ed8e588400.ogg -loglevel quiet -stats -f null - 2>&1 | awk '{print $2}' | sed s/://g | sed s/[a-z]//g | sed s/=//g")
			#sed 's|[^0-9]||g'")
			#made= made.convert_to(string)
			#print(made.split('='))
			#print(type(made))
			#if time=00:00:30.00 <= made
			#	print("Yeehaw")
			#return made
			#print(type(var))
		else: 
			return audio.info.length
	if fname.endswith(".m4a"):
		from mutagen.mp4 import MP4
		audio = MP4(fname)
		return audio.info.length

print(length_wav('/Users/catherineng/Downloads/0aeaedfc-b0ee-4ad1-a6b7-85ed8e588400.ogg'))

""" elif ".m4a" in f:
	for (dirpath, dirnames, filenames) in os.walk("/Users/catherineng/Desktop/Python_Projects/huntercodefest/app/static/uploaded_files", topdown= True):
		for filename in filenames: 
			if filename.endswith('.m4a'):
				filepath = dirpath  + '/' + filename
				(path, file_extension) = os.path.splitext(filepath)
				print((path, file_extension)) #('/Users/catherineng/Desktop/Python_Projects/huntercodefest/app/static/uploaded_files/Rewrite', '.m4a')
				file_extension_final = file_extension.replace('.', '')
				print(file_extension_final) #m4a
				try:
					track = AudioSegment.from_file(filepath, file_extension_final)
					#print(track)
					wav_filename = filename.replace(file_extension_final, 'wav')
					print(wav_filename) #Rewrite.wav
					wav_path = dirpath + '/' + wav_filename
					print('CONVERTING: ' + str(filepath))
					file_handle = track.export(wav_path, format='wav')
					os.remove(filepath)
				except:
					print("ERROR CONVERTING " + str(filepath))
	AUDIO_FILE = f
	r = sr.Recognizer()
	with sr.AudioFile(AUDIO_FILE) as source:
			audio = r.record(source)
	transcription = r.recognize_google(audio) #class 'str'
	return transcription """
"""     elif ".m4a" in f: 
		os.system("ffmpeg -i -codec:v copy -codec:a libmp3lame -q:a 2 peacocks.m4a peacocks.mp3")
		sound = AudioSegment.from_mp3(f)
		#root.destroy()
		#filenm = input("What file would you like to export as(wav)? ")
		sound.export("transcript.wav", format="wav")
		AUDIO_FILE = "transcript.wav"
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)
		#print("Transcription: " + r.recognize_google(audio))
		transcription = r.recognize_google(audio) #class 'str'
		return transcription """

'''def make_bargraph_matplot(keys, values):
		fig= Figure()
	ax = fig.subplots()
	width = 0.75
	#ax.plot([1,2])
	#fig, ax = plt.subplots()
	ax.barh(keys, values, width, color = "blue")
	# Set common labels
	ax.set_title('Audio-Number of times words were said')
	ax.set_xlabel('Number of times')
	ax.set_ylabel('Words')
	#fig = plt.bar(*zip(*data.items()), label = "Word counts")
	#plt.xticks(rotation='vertical')
	#plt.tight_layout() 
	buf = io.BytesIO()
	fig.savefig(buf, format="png")
	#buf.seek(0)
	img_64 = base64.b64encode(buf.getbuffer()).decode('ascii')
	return img_64'''
import subprocess
import shlex
import json

def get_length_file(filename):
	# #cmd = 'ffprobe -show_entries format=duration -v quiet -of csv="p=0"'
	cmd = 'ffprobe -show_entries stream=channels -select_streams a:0 -of compact=p=0:nk=1 -v 0'
	args = shlex.split(cmd)
	args.append(filename)
	# # run the ffprobe process, decode stdout into utf-8 & convert to JSON
	ffprobe_output = subprocess.check_output(args).decode('utf-8')

	ffprobe_output = json.loads(ffprobe_output)

	return ffprobe_output
	# cmd = os.system('ffprobe -i -show_entries format=duration -v quiet -of csv="p=0"')
	# return cmd 
#print(get_length_file("/Users/catherineng/Desktop/Python_Projects/huntercodefest/output6.wav"))
#print(get_length_file("/static/uploaded_files/output6.wav"))



import subprocess
import shlex
import json

filename = "/Users/catherineng/Desktop/Python_Projects/huntercodefest/output6.wav"
def get_duration(filename):
	#cmd = 'ffprobe -show_entries format=duration -v quiet -of csv="p=0"'
	cmd = 'ffprobe -show_entries stream=channels -select_streams a:0 -of compact=p=0:nk=1 -v 0'
	args = shlex.split(cmd)
	args.append(filename)
	# run the ffprobe process, decode stdout into utf-8 & convert to JSON
	ffprobe_output = subprocess.check_output(args).decode('utf-8')

	ffprobe_output = json.loads(ffprobe_output)

	return ffprobe_output
#print(get_duration(filename))

import numpy as np
from wordcloud import WordCloud, ImageColorGenerator

from PIL import Image
import matplotlib.pyplot as plt

text = "I would love to try or hear the sample audio your app can produce. I   do not want to purchase, because I've purchased so many apps that say they do something and do not deliver. What does it mean to be an American? In my eyes to be an American means to have privileges, rights, and freedom. America isn't perfect, but it is one of the only countries that have rights given to people of different diversities and gender. America does not have tremendous poverty. Instead we have choices given to us by the people who fought and died for the American people. Without George Washington and the other patriots who planted the first seed in the ground and help plant the American nation we live in now who knows what America would be like now. The people in America are given something that not everybody's given. A chance to be successful and to survive, and most countries are not given that chance. Being in America offers a lot to the people. One of the most important right America offers to America is the chance to be ourselves and to live in a place were small wars are not going on between states or communities. The U.S. gives us a chance to be fed. The people in America are not surrounded by a majority of starving people. Instead we have one of the most powerful economy in the world. America offers so much to the people who live in the U.S., but America will always be full of criticism, violence, and people who are offended by everything. America still seems to manage to be one of the world's best nations. The first Americans planned America to be as successful as it is, but for America to be more peaceful."

""" def get_wordcloud(text, mask_image="static/img/italy_flag.png"):
	#if mask_image is None:
	#Image.open("italy_flag.png").convert('RGB')
	mask = np.array(Image.open("italy_flag.png").convert('RGB'))
	pil_img = WordCloud(width=1600, height=800, mask = mask, background_color = 'white', mode="RGBA", max_font_size=600).generate(text=text)
	#wordcloud = WordCloud(mask=mask, font_path=fpath)
	image_colors = ImageColorGenerator(mask)
	plt.figure(figsize=[7,7])
	plt.imshow(pil_img.recolor(color_func=image_colors), interpolation='bilinear')
	plt.show()
	#return plt

	else:
		mask = np.array(Image.open(mask_image))
		pil_img = WordCloud( mask = mask_image, width=1600, height=800, background_color = 'white', max_font_size=600).generate(text=text)
		image_colors = ImageColorGenerator(mask) """

	#pil_img = WordCloud(font_path=font_path, mask = mask, background_color = 'white', max_font_size=600).generate(text=text).to_image()
	#plt.axis("off")


#get_wordcloud(text, mask_image="static/img/french_flag.png")
def get_wordcloud(text):
    if request.form.get["language"] = "chinese":
		mask_image="static/img/china_flag.jpg"
		mask = np.array(Image.open(mask_image).convert('RGB'))
		pil_img = WordCloud(width=1600, height=800, mask = mask, scale = 50, background_color = 'white', mode="RGBA", max_font_size=600).generate(text=text)
		#wordcloud = WordCloud(mask=mask, font_path=fpath)
		image_colors = ImageColorGenerator(mask)
		plt.figure(figsize=[7,7])
		plt.imshow(pil_img.recolor(color_func=image_colors), interpolation='bilinear')
		plt.axis("off")
		plt.show()
	elif request.form.get["language"] = "american":
    	mask_image="static/img/american_flag.png"
		mask = np.array(Image.open(mask_image).convert('RGB'))
		pil_img = WordCloud(width=1600, height=800, mask = mask, scale = 50, background_color = 'white', mode="RGBA", max_font_size=600).generate(text=text)
		#wordcloud = WordCloud(mask=mask, font_path=fpath)
		image_colors = ImageColorGenerator(mask)
		plt.figure(figsize=[7,7])
		plt.imshow(pil_img.recolor(color_func=image_colors), interpolation='bilinear')
		plt.axis("off")
		plt.show()
	elif request.form.get["language"] = "french":
        mask_image="static/img/france_flag.png"
		mask = np.array(Image.open(mask_image).convert('RGB'))
		pil_img = WordCloud(width=1600, height=800, mask = mask, scale = 50, background_color = 'white', mode="RGBA", max_font_size=600).generate(text=text)
		#wordcloud = WordCloud(mask=mask, font_path=fpath)
		image_colors = ImageColorGenerator(mask)
		plt.figure(figsize=[7,7])
		plt.imshow(pil_img.recolor(color_func=image_colors), interpolation='bilinear')
		plt.axis("off")
		plt.show()
	elif request.form.get["language"] = "spanish":
        mask_image="static/img/spain_flag.png"
		mask = np.array(Image.open(mask_image).convert('RGB'))
		pil_img = WordCloud(width=1600, height=800, mask = mask, scale = 50, background_color = 'white', mode="RGBA", max_font_size=600).generate(text=text)
		#wordcloud = WordCloud(mask=mask, font_path=fpath)
		image_colors = ImageColorGenerator(mask)
		plt.figure(figsize=[7,7])
		plt.imshow(pil_img.recolor(color_func=image_colors), interpolation='bilinear')
		plt.axis("off")
		plt.show()

get_wordcloud(text)