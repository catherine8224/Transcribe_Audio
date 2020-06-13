# importing libraries 
import speech_recognition as sr; import os; from pydub import AudioSegment 
import io; from scipy.io.wavfile import write; import numpy as np
#from pydub.silence import split_on_silence 
from pydub.utils import make_chunks; import re; from google.cloud import storage

def length(fname): #finding the length of audio file
	storage_client = storage.Client()
	bucket = storage_client.get_bucket('awesome-bucketness')
	bb = bucket.get_blob(fname) #Retrieve blob after uploading to GCS
	bblength = bb.download_as_string()
	audio = AudioSegment.from_file(io.BytesIO(bblength), format=re.split('\.', fname)[1]) #also good with wav, m4a, ogg
	if audio is None: #var = os.system("ffmpeg -i /Users/catherineng/Downloads/0aeaedfc-b0ee-4ad1-a6b7-85ed8e588400.ogg -loglevel quiet -stats -f null - 2>&1 | awk '{print $2}' | sed s/://g | sed s/[a-z]//g | sed s/=//g")
		var = system("ffmpeg -i " + fname + " -loglevel quiet -stats -f null - 2>&1 | awk '{print $2}' | sed s/://g | sed s/[a-z]//g | sed s/=//g")
		return var
	else: 
		return audio.duration_seconds #return audio.info.length
	
def transcribe_audio(f, name, lang):
	song = AudioSegment.from_file(io.BytesIO(f), re.split('\.', name)[1])
	audio_chunk = np.array(song.get_array_of_samples()) #convert it to array.array
	audio_chunk = audio_chunk.reshape(song.channels, -1, order='F').T
	output = io.BytesIO(); rate = song.frame_rate
	write(output, rate, audio_chunk)
	r = sr.Recognizer()
	with sr.AudioFile(output) as source:
		audio = r.record(source)
	transcription = r.recognize_google(audio, language=lang) #class 'str'
	return transcription

# a function that splits the audio file into chunks and applies speech recognition 
def silence_based_conversion(path, name, lang): 	
	# open the audio file stored in the local system as a wav file. 
	song = AudioSegment.from_file(io.BytesIO(path), format=re.split('\.', name)[1])
	# move into the directory to store the audio files. #os.chdir('audio_chunks')
	chunks = make_chunks(song, 30000)
	transcription = ""
	# process each chunk 
	for i, chunk in enumerate(chunks): 
				
		# Create 0.5 (10/10000) seconds silence chunk 
		chunk_silent = AudioSegment.silent(duration = 10) 
	
		# add 0.5 sec silence to beginning and  end of audio chunk. This is done so that it doesn't seem abruptly sliced. 
		audio_chunk = chunk_silent + chunk + chunk_silent 
		audio_chunk = audio_chunk.get_array_of_samples() #convert it to array.array
		audio_chunk= np.array(audio_chunk) #convert it to numpy.ndarray
		#print(audio_chunk.shape) #(5293748,)
		audio_chunk = audio_chunk.reshape(song.channels, -1, order='F').T #reshape to (num of samples, num of channels)
		#print(audio_chunk.shape) #(2, 2646874) --> (2646874, 2)
		#specify the bitrate to be 192 kbps #audio_chunk.export("./chunk" + str(i) + ".wav", format ="wav") 
		output = io.BytesIO()
		#audio_chunk.export(output, formsong.dtyat="wav")
		rate = song.frame_rate
		write(output, rate, audio_chunk)
	
		# create a speech recognition object 
		r = sr.Recognizer() 
	
		# recognize the chunk 
		with sr.AudioFile(output) as source: 
			# remove this if it is not working correctly. 
			#r.adjust_for_ambient_noise(source, duration=5) 
			#audio_listened = r.listen(source) 
			audio = r.record(source) 
		try: 
			#try converting it to text 
			rec = r.recognize_google(audio, language=lang) #write the output to the file. #fh.write(rec+". ") 
		# catch any errors. 
		except sr.UnknownValueError: 
			return "Could not understand audio"
	
		except sr.RequestError as e: 
			return "Could not request results. check your internet connection"

		transcription += rec + " "
	return transcription 
	
	#os.chdir('..') 
	
if __name__ == '__main__': 
	print('Enter the audio file path') 
	path = input() 
	silence_based_conversion(path, 'en-US') 
