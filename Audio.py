import speech_recognition as sr
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
wordcloud.to_file("wordCloud.png")  

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
