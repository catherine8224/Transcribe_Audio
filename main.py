import os
from os import listdir
import urllib.request
#from app import app
from flask import (Blueprint, g, session, Flask, flash, make_response, render_template, redirect, request, url_for, send_file, send_from_directory, session, abort)
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from forms import ContactForm

from io import BytesIO
import io
from flask_wtf.csrf import CSRFProtect
app = Flask(__name__)
app.secret_key = 'very secret'
CSRFProtect(app)

import nltk.data
import pdb 
from transcribe import transcribe_audio, transcribe_audio_french, transcribe_audio_naspanish, transcribe_audio_chinese, transcribe_google_punct, get_duration, get_duration_channels
#from shortaudio import sample_recognize
#from word_cloud import wordcloud_something
#imports the Google Cloud Client library
from google.cloud import storage
import uuid
from googletrans import Translator

from os import path
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import base64

import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image

import matplotlib
matplotlib.use('agg')
from flask_mail import Message, Mail
from lexrank import summarizing
from lexrank import vader

#import nltk
import random
import string
import re, string, unicodedata
#from nltk.corpus import wordnet as wn
#from nltk.stem.wordnet import WordNetLemmatizer
import wikipedia as wk
from collections import defaultdict
from collections import Counter
from flask_bootstrap import Bootstrap
import plotly
import plotly.graph_objs as go
import subprocess
import shlex
import json



#UPLOAD_FOLDER = '/Users/catherineng/Desktop/Python_Projects/huntercodefest/app'
font_path = 'fonts/STFangSong.ttf'
font_paths = ''
app = Flask(__name__)

app.secret_key = "secret key" #used by Flask and extension to keep data safe. Set as a convient value during development, but should be overriden with a random value when deploying.
app.config['UPLOAD_FOLDER'] = 'static/uploaded_files' #where we will store the uploaded files

#from os.path import join, dirname, realpath

bootstrap = Bootstrap(app)


#UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads/..')

#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
mail = Mail()

 
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'cathygreat828@gmail.com'
app.config["MAIL_PASSWORD"] = 'WenTiDoc456'
 
mail.init_app(app)

ALLOWED_EXTENSIONS = set(['wav', 'flac', 'mp3', 'm4a', 'ogg', '.3gp', '3g'])

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/catherineng/Downloads/My Project 52130-da00a565db68.json"

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/thanks")
def thanks():
	return render_template("thanks.html")

import pdb
@app.route("/result", methods=[ 'GET', 'POST'])
def result():
	global youtube_id  
	global output
	global video_title
	global graphs 
	#global clouds
	global filepaths
	global uploaded_files
	#if form.validate_on_submit():
	if request.method == 'POST':
		if "subject" in request.form: #request.form.get("subject")=="Results":
			return render_template('result.html', filepaths = filepaths, len = len(uploaded_files), output=output, graphs = graphs)

import pdb
@app.route("/result", methods=[ 'GET', 'POST'])
def boon():
	pdb.set_trace()
	# if request.method == 'GET':
	# 	#clouds = []
	# 	pdb.set_trace()
	# 	value = request.form.get('tvalue')
	# 	return render_template('result.html', value = value, filepaths = filepaths, len = len(uploaded_files), output=output, clouds = clouds, graphs = graphs)
	# elif request.method == 'POST':
	# 	pdb.set_trace()
	# 	value = request.form.get('tvalue')
	# 	return render_template('result.html', value = value, filepaths = filepaths, len = len(uploaded_files), output=output, clouds = clouds, graphs = graphs)
	if request.method=='POST': 
		value = request.form.get('tvalue')
		return str(value)
			# 	for i in range(0, len(uploaded_files)):
			# 	#mask_image="static/img/china_flag.jpg"
			# 		cloud = get_wordcloud(output[i])
			# 		clouds.append(cloud)
			# 		return render_template('result.html', filepaths = filepaths, len = len(uploaded_files), output=output, clouds = clouds, graphs = graphs)
			# elif request.form('tvalue') == "Spanish":
			# 	for i in range(0, len(uploaded_files)):
			# 	#mask_image="static/img/american_flag.png"
			# 		cloud = get_wordcloud(output[i])
			# 		clouds.append(cloud)
			# 		return render_template('result.html', filepaths = filepaths, len = len(uploaded_files), output=output, clouds = clouds, graphs = graphs)
			# elif "Chinese" in request.form:
			# 	for i in range(0, len(uploaded_files)):
			# 	#mask_image="static/img/france_flag.png"
			# 		cloud = get_wordcloud(output[i])
			# 		clouds.append(cloud)
			# 		return render_template('result.html', filepaths = filepaths, len = len(uploaded_files), output=output, clouds = clouds, graphs = graphs)
			# elif "English" in request.form:
			# 	for i in range(0, len(uploaded_files)):
			# 	#mask_image="static/img/spain_flag.png"
			# 		cloud = get_wordcloud(output[i])
			# 		clouds.append(cloud)
			# 		return render_template('result.html', filepaths = filepaths, len = len(uploaded_files), output=output, clouds = clouds, graphs = graphs)

			#else: 
			#	return render_template('result.html', filepaths = filepaths, len = len(uploaded_files), output=output, graphs = graphs)

@app.route("/result_yt", methods=['GET', 'POST'])
def result_yt():
	if request.method == 'POST':
		if "subjectss" in request.form:
			return render_template("result_yt.html", ebu = youtube_id, textsent = sent, lexyranky = lexyranky, cloud =cloud, bar_graph = bar_graph, sentence= sentence)


#Contact Us Form
@app.route("/contact", methods= ['GET', 'POST'])
def contact():
	form = ContactForm()
	if request.method == 'POST':
		if form.validate_on_submit() == False:
			flash('All fields are required.')
			return render_template('contact.html', form=form)
		else:
			msg = Message(form.subject.data, sender='contact@example.com', recipients=['cathygreat828@gmail.com'])
			msg.body = """
			From: %s %s <%s>
			%s
			""" % (form.firstname.data, form.lastname.data, form.email.data, form.message.data)
			msg.attach(
			form.audiofile.data.filename,
			'application/octect-stream',
			form.audiofile.data.read())
			mail.send(msg)

			return render_template("contact.html", success=True)
 
	elif request.method == 'GET':
		return render_template('contact.html', form=form)

@app.route("/start")
def start():
	response = make_response(redirect('/'))
	session_id = uuid.uuid4().hex
	response.set_cookie('session_id', session_id)
	return response

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

userdict_list = ['阿Ｑ', '孔乙己', '单四嫂子']

def jieba_processing_txt(text):
	import jieba
	#jieba.enable_parallel(4)
	# Setting up parallel processes :4 ,but unable to run on Windows
	for word in userdict_list:
		jieba.add_word(word)

	mywordlist = []
	seg_list = jieba.cut(text, cut_all=False)
	liststr = "/ ".join(seg_list)

	for myword in liststr.split('/'):
		if len(myword.strip()) > 1:
			mywordlist.append(myword)
	return ' '.join(mywordlist)

def get_wordcloud_ch(text):
	wc = WordCloud(font_path=font_path, background_color="white", max_words=2000, #mask=back_coloring,
	max_font_size=100, random_state=42, width=1000, height=860, margin=2,).generate(jieba_processing_txt(text)).to_image()
	img = io.BytesIO()
	wc.save(img, "PNG")
	#wordcloud.to_image().save(img, 'PNG')
	img.seek(0)
	img_64 = base64.b64encode(img.getvalue()).decode('utf-8')
	#data = base64.b64encode(img.getbuffer()).decode("ascii")
	return img_64

#def get_wordcloud(text, mask_image="static/img/french_flag.png"):

def get_wordcloud(text):
 	#text = text.decode("utf-8")
	mask = np.array(Image.open("static/img/french_flag.png").convert('RGB'))
	pil_img = WordCloud(width=1600, height=800, mask = mask, scale = 50, background_color = 'white', mode="RGBA", max_font_size=600).generate(text=text)
	image_colors = ImageColorGenerator(mask)
	plt.figure(figsize=[7,7])
	plt.imshow(pil_img.recolor(color_func=image_colors), interpolation='bilinear')
	plt.axis("off")
	plt.imshow(pil_img, interpolation='bilinear')
	plt.tight_layout(pad=0)
 	#save it to a temporary buffer
	img = io.BytesIO()
	pil_img.save(img, "PNG")
	img.seek(0)
	img_64 = base64.b64encode(img.getvalue()).decode('utf-8')
	return img_64

def word_counts(str): 
	counts = dict()
	words = str.split()

	for word in words:
		if word in counts:
			counts[word] += 1
		else:
			counts[word] = 1
	return counts

from matplotlib.font_manager import FontProperties 
chinese = FontProperties(fname=r'/Library/Fonts/Microsoft/SimHei.ttf', size=20) 
font_name= FontProperties('Heiti TC')
def make_bar_ch(keys, values):
	fig= Figure()
	ax = fig.subplots()
	width = 0.60
	#barh plots horizontal barplot
	ax.bar(keys, values, width)
	# Set common labels
	ax.set_title(u'说的字数', fontproperties=font_name) 
	ax.set_xlabel(u'次数',fontproperties=font_name)
	ax.set_ylabel(u'字', fontproperties=font_name)
	ax.set_xticks(keys)
	for label in ax.xaxis.get_majorticklabels():
		label.set(fontproperties=font_name)
	#set parameters for tick labels
	ax.tick_params(axis='x', which='major', labelsize=5, grid_linewidth = 100)
	#plt.xticks(keys, fontproperties=chinese) 
	buf = BytesIO()
	fig.savefig(buf, format="png")
	#img_64 = base64.b64encode(buf.getbuffer()).decode('ascii')
	img_64 = base64.b64encode(buf.getbuffer()).decode('utf-8')
	#data = base64.b64encode(img.getbuffer()).decode("ascii")
	return img_64

def make_bargraph(keys, values):
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
	f, ax = plt.subplots(figsize=(11, 9)) # this creates a figure 11 inch wide, 9 inch high
	ax = sns.barplot(values, keys)
	ax.set(xlabel="Number of times", ylabel='Words')
	# Set common labels
	#ax.set_title('Audio-Number of times words were said')
	#ax.set_xlabel('Number of times')
	#ax.set_ylabel('Words')
	fig = ax.get_figure()
	#fig.savefig('bargraph.png')
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
	return result

#Youtube Captions 
import re
import html2text

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def deEmojify(inputString):
	return inputString.encode('ascii', 'ignore').decode('ascii')

@app.route('/youtube')
def youtube_form():
	return render_template('youtube.html')

from flask import Flask, send_file, make_response

#Where I Upload Multiple Audio Files--only for wav files
def length_wav(fname): #finding the length of audio file
	if fname.endswith(".wav") or fname.endswith(".WAV"):
		import wave
		import contextlib	
		with contextlib.closing(wave.open(fname,'r')) as f:
			frames = f.getnframes()
			rate = f.getframerate()
			duration = frames / float(rate)
		return duration
	if fname.endswith(".mp3") or fname.endswith(".MP3"):
		from mutagen.mp3 import MP3
		audio = MP3(fname)
		if audio is None: 
			var = os.system("ffmpeg -i /Users/catherineng/Downloads/0aeaedfc-b0ee-4ad1-a6b7-85ed8e588400.ogg -loglevel quiet -stats -f null - 2>&1 | awk '{print $2}' | sed s/://g | sed s/[a-z]//g | sed s/=//g")
			return var
		else: 
			return audio.info.length
	if fname.endswith(".flac"):
		from mutagen.flac import FLAC
		audio = FLAC(fname)
		if audio is None: 
			var = os.system("ffmpeg -i /Users/catherineng/Downloads/0aeaedfc-b0ee-4ad1-a6b7-85ed8e588400.ogg -loglevel quiet -stats -f null - 2>&1 | awk '{print $2}' | sed s/://g | sed s/[a-z]//g | sed s/=//g")
			return var
		else: 
			return audio.info.length
	if fname.endswith(".ogg"):
		import mutagen
		audio = mutagen.File(fname)
		if audio is None: 
			var = os.system("ffmpeg -i /Users/catherineng/Downloads/0aeaedfc-b0ee-4ad1-a6b7-85ed8e588400.ogg -loglevel quiet -stats -f null - 2>&1 | awk '{print $2}' | sed s/://g | sed s/[a-z]//g | sed s/=//g")
			return var
		else: 
			return audio.info.length
	if fname.endswith(".m4a"):
		from mutagen.mp4 import MP4
		audio = MP4(fname)
		if audio is None: 
			var = os.system("ffmpeg -i /Users/catherineng/Downloads/0aeaedfc-b0ee-4ad1-a6b7-85ed8e588400.ogg -loglevel quiet -stats -f null - 2>&1 | awk '{print $2}' | sed s/://g | sed s/[a-z]//g | sed s/=//g")
			return var
		else: 
			return audio.info.length

#CREATE DOUBLE BARPLOT AND REGULAR BAR PLOT
def creates_plot(features):
	import plotly
	import plotly.graph_objs as go
	import pandas as pd
	import numpy as np
	import json
	if features == 'Double barplot':
		#datas = word_counts(output[0].lower()) 
		#print("DATA: ", text)
		#print("DATAS: ", text)
		datas = word_counts(sentence.lower()) 
		#sentence = self.cleaning_lyrics()
		data = [
			go.Bar(
				name = 'First Youtube Link', 
				x= list(datas), # assign x as the dataframe column 'x'
				y= list(datas.values()),
				width= 0.4, 
				offset = -0.4
			),
			go.Bar(
				name='Second Youtube Link', 
				x=list(datas), 
				y=list(datas.values()),
				width=0.4, 
				offset = -0.4
			)
		]
		graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

	else:
		# N = 1000
		# random_x = np.random.randn(N)
		# random_y = np.random.randn(N)
		datas = word_counts(sentence.lower()) 

		#sentence = self.cleaning_lyrics()
		data = [
			go.Bar(
				name = video_title, 
				width=0.4, 
				offset = 0.0,
				x= list(datas), # assign x as the dataframe column 'x'
				y= list(datas.values())
			)
		]
	graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON

@app.route('/bar', methods=['GET', 'POST'])
def changes_features():
	features = request.args['selected']
	graphJSON= creates_plot(features)
	return graphJSON

@app.route("/", )
def indexs():
	features = 'Scatter'
	bar = creates_plot(features)
	return render_template("") 
import simplejson

#CREATE DOUBLE BARPLOT AND REGULAR BAR PLOT
def create_plot(feature):
	import plotly
	import plotly.graph_objs as go
	import pandas as pd
	import numpy as np
	import json
	if feature == 'Double barplot':
		datas = word_counts(output[0].lower()) 
		datass = word_counts(output[1].lower()) 
		print("DATA: ", datas)
		print("DATAS: ", datass)
		#sentence = self.cleaning_lyrics()
		data = [
			go.Bar(
				name = 'First File Upload', 
				x= list(datas), # assign x as the dataframe column 'x'
				y= list(datas.values()),
				width= 0.4, 
				offset = -0.4
			),
			go.Bar(
				name='Second Youtube Link', 
				x=list(datass), 
				y=list(datass.values()),
				width=0.4, 
				offset = -0.4
			)
		]
		#fig.update_layout(barmode='stack')

		graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

	else:
		datas = word_counts(output[0].lower()) 

		#sentence = self.cleaning_lyrics()
		data = [
			go.Bar(
				name = 'First File Upload', 
				x= list(datas), # assign x as the dataframe column 'x'
				y= list(datas.values())
			)
		]
	graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON


@app.route('/bar', methods=['GET', 'POST'])
def change_features():
	feature = request.args['selected']
	graphJSON= create_plot(feature)
	return graphJSON

@app.route("/", )
def index():
	feature = 'Scatter'
	bar = create_plot(feature)
	return render_template("") 
import simplejson

import requests

def cleaning_lyrics(youtube_id):
	global sentence
	#global youtube_id
	Lyrics_URL = "http://video.google.com/timedtext?type=list&v=" + youtube_id 
	Lyrics = requests.get(Lyrics_URL)
	Lyrics = Lyrics.text
	if 'name=""' in Lyrics:
		lyrics_url = "http://video.google.com/timedtext?lang=en&v=" + youtube_id
		lyrics = requests.get(lyrics_url)
		texts= lyrics.text
		texts = cleanhtml(texts)
		texts = deEmojify(texts)
		texts = texts.replace('&lt;font color=&quot;#FFFFFF&quot;&gt;&lt;i&gt;', " ")
		texts = texts.replace('&lt;/i&gt;&lt;/font&gt;', " ")
		texts = texts.replace('&amp;#39;', "'")
		texts = texts.replace('&amp;quot;', '"')
		texts = texts.replace('\n', ' ')
		marscapone = re.sub("(?!^)(?=\s\s)", ".", texts).lower()
		sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
		sentences = sent_tokenizer.tokenize(marscapone)
		sentences = [sent.capitalize() for sent in sentences]
		sentence = ' '.join(sentences)
		return sentence
	elif '"English"' in Lyrics: 
		lyrics_url = "http://video.google.com/timedtext?name=en&lang=en&v=" + youtube_id
		lyrics = requests.get(lyrics_url)
		texts= lyrics.text
		texts = cleanhtml(texts)
		texts = deEmojify(texts)
		texts = texts.replace('&lt;font color=&quot;#FFFFFF&quot;&gt;&lt;i&gt;', " ")
		texts = texts.replace('&lt;/i&gt;&lt;/font&gt;', " ")
		texts = texts.replace('&amp;#39;', "'")
		texts = texts.replace('&amp;quot;', '"')
		texts = texts.replace('\n', ' ')
		marscapone = re.sub("(?!^)(?=\s\s)", ".", texts).lower()
		sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
		sentences = sent_tokenizer.tokenize(marscapone)
		sentences = [sent.capitalize() for sent in sentences]
		sentence = ' '.join(sentences)
		return sentence

import pdb
def sample_long_running_recognize(storage_uri):
	from google.cloud import speech_v1
	#from google.cloud import speech_v1p1beta1
	from google.cloud.speech_v1 import enums
	import io
	import os
	from google.cloud import speech
	client = speech_v1.SpeechClient()
	#client = speech_v1p1beta1.SpeechClient()
	#storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.raw'
	#The number of channels in the input audio file (optional)
	
	audio_channel_count = get_duration_channels(filepath)
	enable_separate_recognition_per_channel = True

	# Sample rate in Hertz of the audio data sent
	#sample_rate_hertz = 44100#16000
	sample_rate_hertz = get_duration(filepath)
	# The language of the supplied audio
	language_code = "en-US"

	# Encoding of audio data sent. This sample sets this explicitly.
	# This field is optional for FLAC and WAV audio formats.
	encoding = enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED
	config = {
		"audio_channel_count": audio_channel_count,
		"enable_separate_recognition_per_channel": enable_separate_recognition_per_channel,
		"sample_rate_hertz": sample_rate_hertz,
		"language_code": language_code,
		#"alternative_language_codes": alternative_language_codes,
		"encoding": encoding,
	}
	audio = {"uri": storage_uri}

	operation = client.long_running_recognize(config, audio)

	print(u"Waiting for operation to complete...")
	response = operation.result()

	stored_data = []
	for result in response.results:
		# First alternative is the most probable result
		alternative = result.alternatives[0]
		#print(type(alternative)) #<class 'google.cloud.speech_v1.types.SpeechRecognitionAlternative'> #None   #<class 'google.cloud.speech_v1.types.SpeechRecognitionAlternative'>
		alternatives = alternative.transcript
		#print(type(alternatives))
		stored_data.append(alternatives)
		data = ' '.join(stored_data[::2])
		#alternative = alternative.transcript
		#print("RESULT: " , result)
		#print("Alternative: ", alternative)
		#print(u"Transcript: {}".format(alternative.transcript))
	return data
	

	# When set to true, each audio channel will be recognized separately.
	# The recognition result will contain a channel_tag field to state which
	# channel that result belongs to
	

@app.route("/youtube", methods=['GET', 'POST'])
def youtube():
	global youtube_id  
	global output
	global video_title
	global graphs 
	#global clouds
	global filepaths
	global uploaded_files
	global filepath
	global sent
	global lexyranky
	#global cloud
	global bar_graph
	global sentence
	import sys
	import os 
	if request.method == 'POST':
		if request.form.get("Analyze") == 'Youtube':
			counter = 0 
			text = request.form['Text']
			if ',' in text:
				bloggy= text.split(",", 1)
				output = []
				for i in range(len(bloggy)):
					if 'https://www.youtube.com/watch?v=' not in bloggy[i]:
						flash('Not a YouTube link. Please upload a YouTube link')
						return redirect(request.url)
					elif text == '':
						flash('No selected YouTube link inputted ')
						return redirect(request.url)
					youtube_id= bloggy[i].split("=", 1)[1]
					Lyrics_URL = "http://video.google.com/timedtext?type=list&v=" + youtube_id 
					Lyrics = requests.get(Lyrics_URL)
					Lyrics = Lyrics.text
					#if 'name=""' in Lyrics or 'name="en"'  in Lyrics:
					s = cleaning_lyrics(youtube_id)
					output.append(s)
					lexyranky = summarizing(s)
					sent = vader(s)
					cloud = get_wordcloud(s)
					data = word_counts(s.lower()) 
					keys = list(data)
					values= list(data.values())
					#Make Bar Graph 
					bar_graph= make_bargraph(keys, values)
				flash('File(s) successfully uploaded')
				return render_template("youtube.html", text = output)
			elif ',' not in text:
				youtube_id= text.split("=", 1)[1]
				video_url = "https://www.youtube.com/watch?v=" + youtube_id
				import lxml
				from lxml import etree
				import urllib.request
				youtube = etree.HTML(urllib.request.urlopen(video_url).read()) #enter your youtube url here
				video_title = youtube.xpath("//span[@id='eow-title']/@title") #get xpath using firepath firefox addon
				#''.join(video_title)
				Lyrics_URL = "http://video.google.com/timedtext?type=list&v=" + youtube_id 
				Lyrics = requests.get(Lyrics_URL)
				Lyrics = Lyrics.text
				if 'name=""' in Lyrics or 'name="en"' in Lyrics:
					sentence = cleaning_lyrics(youtube_id)
					lexyranky = summarizing(sentence)
					sent = vader(sentence)
					cloud = get_wordcloud(sentence)
					data = word_counts(sentence.lower()) 
					keys = list(data)
					values= list(data.values())
					#Make Bar Graph 
					bar_graph= make_bargraph(keys, values)
					flash('File(s) successfully uploaded')
				return render_template("youtube.html", sent = sent, lexyranky = lexyranky, cloud =cloud, bar_graph = bar_graph, text= sentence)
			else:
				sounds_dir_path = "/music/sounds/"
				sound_path = sounds_dir_path + str(counter).zfill(4)
				os.system('youtube-dl --extract-audio --audio-format mp3 --prefer-ffmpeg -o' + os.getcwd() + sound_path + ".m4a " + video_url)
				sentence = "Could not transcribe! I have downloaded the YouTube link as an mp3 file in the /music/sounds folder. Please go to the 'Upload' link to upload the mp3 file and try to transcribe the audio there."
				counter += 1
				filepath = os.getcwd() + sound_path + ".m4a " + video_url
				return render_template("youtube.html", filepath= filepath, text=sentence)
		elif request.form.get("Analyze") == 'File':
			graphs = []
			#clouds = []
			output = []
			filepaths = []
			import pdb
			if 'file[]' not in request.files:
				flash('No file part')
				return redirect(request.url)
			uploaded_files = request.files.getlist('file[]')
			#print(simplejson.dumps({"files": [result.get_file()]}))
			for file in uploaded_files:
				if file and allowed_file(file.filename):
					filename = secure_filename(file.filename)
					print("File Name: ", filename)
					filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
					print("FILE PATH: ", filepath)
					filepaths.append(filepath)
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					name = '{}'.format(filename)
					storage_client = storage.Client()
					bucket = storage_client.get_bucket('awesome-bucketness')
					blob = storage.Blob(name, bucket)
					#blob = bucket.blob()
					blob.upload_from_filename(filepath)
					with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
						#pdb.set_trace()
						if length_wav(filepath) <=30 or length_wav(filepath) <= 000030.00: #filename.endswith(".mp3") and 
							if 'fr' in filename:
								output.append(transcribe_audio_french(filepath))
							elif 'sp' in filename:
								output.append(transcribe_audio_naspanish(filepath))	
							elif 'ch' in filename:
								output.append(transcribe_audio_chinese(filepath))
							else:
								output.append(transcribe_audio(filepath)) #output.append(transcribe_google_punct(filepath)) 	#print(filename) <FileStorage: 'transcript-sp.mp3' ('audio/mp3')>   <FileStorage: 'transcript.mp3' ('audio/mp3')>
						elif length_wav(filepath) > 30 or length_wav(filepath) > 000030.00: #filename.endswith(".wav") and 
							if 'fr' in filename:
								output.append(transcribe_audio_french(filepath))
							elif 'sp' in filename:
								output.append(transcribe_audio_naspanish(filepath))	
							elif 'ch' in filename:
								output.append(transcribe_audio_chinese(filepath))
							else:
								output.append(sample_long_running_recognize("gs://awesome-bucketness/" + filename))
							#pdb.set_trace()
						print("OUTPUT:", output)
			for i in range(0, len(uploaded_files)):
				#print("LENGTH: ", len(uploaded_files))
				filename = secure_filename(file.filename)
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
					#pdb.set_trace()
					#cloud = get_wordcloud(output[i])
					#clouds.append(cloud)
					data = word_counts(output[i].lower()) 
					keys = list(data)
					values= list(data.values())
					#Make Bar Graph 
					bar_graph= make_bargraph(keys, values)
					graphs.append(bar_graph)  
			flash('File(s) successfully uploaded')
			return render_template('youtube.html', filepaths = filepaths, lens = len(filepaths), len = len(uploaded_files), output=output, graphs = graphs) #clouds = clouds,
		return ''

@app.route('/record_form')
def record_form():
	return render_template('record.html')

@app.route('/record_form', methods=['POST'])
def upload():
	#session_id = request.cookies.get('session_id')
	word= request.args.get('word')
	audio_data = request.data
	filename = word + '.wav'
	secure_name= secure_filename(filename)
	gcs = storage.Client()
	bucket = gcs.get_bucket('awesome-bucketness')
	blob = storage.Blob(secure_name, bucket)
	blob.upload_from_string(audio_data, content_type='audio/wav')
	return make_response('All good')

# CSRF protection, see http://flask.pocoo.org/snippets/3/.
# @app.before_request
# def csrf_protect():
#     if request.method == "POST":
#         token = session['_csrf_token']
#         if not token or token != request.args.get('_csrf_token'):
#             abort(403)

# def generate_csrf_token():
#     if '_csrf_token' not in session:
#         session['_csrf_token'] = uuid.uuid4().hex
#     return session['_csrf_token']

# app.jinja_env.globals['csrf_token'] = generate_csrf_token

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
							   'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
	app.run(debug=True)
  #We made two new changes



#import main


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/catherineng/Downloads/My Project 52130-da00a565db68.json"


