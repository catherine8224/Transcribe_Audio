import speech_recognition as sr
from os import path
from pydub import AudioSegment
import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf 

from tkinter import filedialog
from tkinter import *

def transcribe_audio(f):
    #root = Tk()
    #root.withdraw()
    #file =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Audio files",".mp3"),("all files","*.*")))
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
    return transcription