import speech_recognition as sr
from os import path
from pydub import AudioSegment
import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf 
import os

#f = "/Users/catherineng/Desktop/Python_Projects/huntercodefest/app/static/uploaded_files/peacocks.wav"

def transcribe_audio(f):
	#for (dirpath, dirnames, filenames) in os.walk("M4a_files/"):
	#filepath = dirpath + '/' + filename
	#root = Tk()
	#root.withdraw()
	#file =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Audio files",".mp3"),("all files","*.*")))
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
		transcription = r.recognize_google(audio) #class 'str'
		return transcription

	elif ".wav" in f: 
		AUDIO_FILE = f
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)
		transcription = r.recognize_google(audio) #class 'str'
		return transcription
	elif ".m4a" in f:
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
		return transcription
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
	
#print(transcribe_audio(f))

def transcribe_audio_french(f):
	if f.endswith(".mp3"):
		sound = AudioSegment.from_mp3(f)
		sound.export("moo.wav", format="wav")

		AUDIO_FILE = "moo.wav"

		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)
		#print("Transcription: " + r.recognize_google(audio))
		transcription = r.recognize_google(audio, language="fr-FR") #class 'str'
		return transcription
	elif f.endswith(".wav"): 
		AUDIO_FILE = f
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
				audio = r.record(source)
		transcription = r.recognize_google(audio, language="fr-FR") #class 'str'
		return transcription
#print(transcribe_audio_french('/Users/catherineng/Desktop/Python_Projects/huntercodefest/app/static/uploaded_files/transcript-fr.mp3'))

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
			
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/catherineng/Downloads/My Project 52130-da00a565db68.json"

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
		encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
		#sample_rate_hertz=8000,
		sample_rate_hertz=22050,
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

#transcribe_google_punct(path)