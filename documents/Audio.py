import speech_recognition as sr
from os import path
from pydub import AudioSegment
import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf 
import os 
from pathlib import Path


''' def transcribe_audio(f):
	print(Path(f).suffix)
	if Path(f).suffix == '.mp3': 
		print("Hola!")
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
		return "Transcript: "+ transcription
	elif Path(f).suffix == '.wav':
		print("Howa!")
		AUDIO_FILE = f

		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)

		#print("Transcription: " + r.recognize_google(audio))
		transcription = r.recognize_google(audio) #class 'str'
		return "Transcript: "+ transcription

#with open('transcript.mp3', 'rb') as f:
#  pat = transcribe_audio(f)

#print(pat)  

F = open('transcript.mp3')
print(transcribe_audio(F)) '''

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
wordcloud.to_file("wordCloud.png")  '''

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


(function(){
	"use strict";
	var $start_button = document.getElementById("recordButton");
	var $stop_button = document.getElementById("stopButton");
	//var $reset_button = document.getElementById("reset-button");
	var $timer = document.getElementById("timer");
	var second = 0;
	function zf(x) { return (x > 9 ? "" : "0") + x; }
	function updateSecond(x) {
		second = x;
		$timer.textContent = zf(second / 60 | 0) + ":" + zf(second % 60);
	}
	function nextSecond() {
		updateSecond(second + 1);
	}
	var timer_handle = -1;
	$start_button.addEventListener("click", function(ev) {
		timer_handle = setInterval(nextSecond, 1000);
	}, false);
	$stop_button.addEventListener("click", function(ev) {
		if (timer_handle != -1) {
			clearInterval(timer_handle);
			timer_handle = -1;
		}
	}, false);
	//$reset_button.addEventListener("click", function(ev) {
		//updateSecond(0);
	//}, false);
})();
'''

import os

def length(fname):
	import wave
	import contextlib
	#filepath = os.system('pwd')
	filepath = os.getcwd()
	print(type(filepath)) #integer
	#filepath = str(filepath)
	filename = filepath + fname
	#print(filename)
	with contextlib.closing(wave.open(filename,'r')) as f:
		frames = f.getnframes()
		rate = f.getframerate()
		duration = frames / float(rate)
		#print(duration)
	return duration

#print(length('/static/uploaded_files/s2.wav'))


def word_counts(str): 
	counts = dict()
	words = str.split()

	for word in words:
		if word in counts:
			counts[word] += 1
		else:
			counts[word] = 1
	return counts

from matplotlib.figure import Figure
from io import BytesIO
import base64
import matplotlib.pylab as plt

string = """ across the sky. Hear the echo saying. "i won't be silenced". . Though you wanna see me. . . Tremble when you try it. . All i know is
i won't go speechless. Speechless!. 'cause i'll breathe. When they try
to suffocate me. . Don't you underestimate me. . 'cause i know that
i won't go speechless. All i know
is i won't go speechless. Speechless!."""

def make_bargraph(keys, values):
	import seaborn as sns
	fig= Figure()
	ax = fig.subplots()
	width = 0.75
	#ax.plot([1,2])
	#fig, ax = plt.subplots()

	#ax.barh(keys, values, width, color = "blue")

	ax = sns.barplot(values, keys)
	ax.set(xlabel="Number of times", ylabel='Words')
	# Set common labels
	#plt.tight_layout()
	#plt.show()
	# ax.set_title('Audio-Number of times words were said')
	# ax.set_xlabel('Number of times')
	# ax.set_ylabel('Words')

	#fig = plt.bar(*zip(*data.items()), label = "Word counts")
	#plt.xticks(rotation='vertical')
	#plt.xlabel('Words')
	#plt.tight_layout() 
	buf = BytesIO()
	fig.savefig(buf, format="png")
	#buf.seek(0)
	#img_64 = base64.b64encode(buf.getbuffer()).decode('utf-8')
	img_64 = base64.b64encode(buf.getbuffer()).decode('ascii')
	return img_64



#data = word_counts(string.lower()) 
#keys = list(data)
#values= list(data.values())
#print(make_bargraph(keys, values))


''' buf = BytesIO()
fig.savefig(buf, format="png")
img_64 = base64.b64encode(buf.getbuffer()).decode('utf-8')
return img_64 '''

def make_bargraph(keys, values):
	import seaborn as sns
	fig= Figure()
	ax = fig.subplots()
	#width = 0.75
	#ax.plot([1,2])
	#fig, ax = plt.subplots()

	#ax.barh(keys, values, width, color = "blue")

	ax = sns.barplot(values, keys)
	ax.set(xlabel="Number of times", ylabel='Words')
	# Set common labels
	#ax.set_title('Audio-Number of times words were said')
	#ax.set_xlabel('Number of times')
	#ax.set_ylabel('Words')

	#fig = plt.bar(*zip(*data.items()), label = "Word counts")
	#plt.xticks(rotation='vertical')
	#plt.xlabel('Words')
	#plt.tight_layout() 
	#buf = BytesIO()
	#fig.savefig(buf, format="png")
	plt.tight_layout()
	plt.show()
	#buf.seek(0)
	#img_64 = base64.b64encode(buf.getbuffer()).decode('utf-8')
	#img_64 = base64.b64encode(buf.getbuffer()).decode('ascii')
	#return img_64

# data = word_counts(string.lower()) 
# keys = list(data)
# values= list(data.values())
# print(make_bargraph(keys, values))

def makes_bargraph(keys, values):
	import seaborn as sns
	import matplotlib.pylab as plt
	import io
	#fig= Figure()
	#ax = fig.subplots()
	sns.set_style("white")
	#width = 0.75
	#ax.plot([1,2])
	#fig, ax = plt.subplots()

	#ax.barh(keys, values, width, color = "blue")
	f, ax = plt.subplots(figsize=(11, 9))
	ax = sns.barplot(values, keys)
	ax.set(xlabel="Number of times", ylabel='Words')
	# Set common labels
	#ax.set_title('Audio-Number of times words were said')
	#ax.set_xlabel('Number of times')
	#ax.set_ylabel('Words')
	fig = ax.get_figure()
	fig.savefig('bargraph.png')
	#fig = plt.bar(*zip(*data.items()), label = "Word counts")
	#plt.xticks(rotation='vertical')
	#plt.xlabel('Words')
	#plt.tight_layout() 
	bytes_image = io.BytesIO()
	plt.savefig(bytes_image, format="png")
	bytes_image.seek(0)
	figdata_png = base64.b64encode(bytes_image.getvalue())
	result = str(figdata_png)[2:-1]
	#img_64 = base64.b64encode(buf.getbuffer()).decode('ascii')
	#img_64 = base64.b64encode(buf.getbuffer()).decode('ascii')
	#return buf
	return result

data = word_counts(string.lower()) 
keys = list(data)
values= list(data.values())
print(makes_bargraph(keys, values))






			'''
			for i in range(len(uploaded_files)):
				if 'ch' in filename:
					words = jieba_processing_txt(output[i])
					cloud = get_wordcloud_ch(words)
					clouds.append(cloud)
					data = Counter(output[i])
					keys = list(data)
					values= list(data.values())
					#Make Bar Graph 
					bar_graph= make_bar_ch(keys, values)
					graphs.append(bar_graph)	
				else:
					lexyranky = summarizing(output[i])
					sent = vader(output[i])
					cloud = get_wordcloud(output[i])
					clouds.append(cloud)
					data = word_counts(output[i].lower()) 
					keys = list(data)
					values= list(data.values())
					#Make Bar Graph 
					bar_graph= make_bargraph(keys, values)
					graphs.append(bar_graph)  
			flash('File(s) successfully uploaded')
			'''

#return render_template('youtube.html', filepaths = filepaths, lens = len(filepaths), len = len(uploaded_files), output=output, clouds = clouds, graphs = graphs, lexyranky = lexyranky, sent= sent)
