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
from transcribe import transcribe_audio, transcribe_audio_french, transcribe_audio_naspanish, transcribe_audio_chinese, transcribe_google_punct
from separate import music_transcription
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
#import warnings
#warnings.filterwarnings("ignore")
#nltk.download('punkt') 
#nltk.download('wordnet')
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.metrics.pairwise import cosine_similarity, linear_kernel

from google_long import sample_long_running_recognize

#UPLOAD_FOLDER = '/Users/catherineng/Desktop/Python_Projects/huntercodefest/app'
font_path = 'fonts/STFangSong.ttf'

app = Flask(__name__)

#CLOUD_STORAGE_BUCKET = os.environ['GCP_PROJECT']

app.secret_key = "secret key" #used by Flask and extension to keep data safe. Set as a convient value during development, but should be overriden with a random value when deploying.
app.config['UPLOAD_FOLDER'] = 'static/uploaded_files' #where we will store the uploaded files
#from os.path import join, dirname, realpath

#UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads/..')

#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
mail = Mail()

 
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'cathygreat828@gmail.com'
app.config["MAIL_PASSWORD"] = 'WenTiDoc456'
 
mail.init_app(app)

ALLOWED_EXTENSIONS = set(['wav', 'flac', 'mp3', 'm4a'])

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

# from chatterbot import ChatBot
# from chatterbot.trainers import ListTrainer
# from chatterbot.trainers import ChatterBotCorpusTrainer
# #create chatbot

# anylanuageBot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
# trainer = ChatterBotCorpusTrainer(anylanuageBot)
# trainer.train("chatterbot.corpus.english", "chatterbot.corpus.spanish", "chatterbot.corpus.custom.website") #train the chatter bot for english

# @app.route("/maiden")
# def maiden():
# 	return render_template("chatbot.html")

# @app.route("/get")
# #function for the bot response
# def get_bot_response():
# 	userText = request.args.get('msg')
# 	reg_ex = re.search('tell me about (.*)', userText)
# 	try:
# 		if reg_ex:
# 			topic = reg_ex.group(1)
# 			wiki = wk.summary(topic, sentences = 3)
# 			return wiki
# 		else: 
# 			return str(anylanuageBot.get_response(userText))
# 	except Exception as e:
# 			print("No content has been found")


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

#@app.route("/")
#def home():
	#session_id = request.cookies.get('session_id')
	#if session_id:
		#all_done = request.cookies.get('all_done')
		#if all_done:  
#    return render_template("record.html")
#    else:
#        return render_template("template.html")
	#return render_template("home.html")


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

	#with open(stopwords_path, encoding='utf-8') as f_stop:
	#    f_stop_text = f_stop.read()
	#    f_stop_seg_list = f_stop_text.splitlines()

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

def get_wordcloud(text, mask_image="static/french_flag.png"):
	#text = text.decode("utf-8")
	if mask_image is not None:
		mask = np.array(Image.open(mask_image))
		pil_img = WordCloud(font_path=font_path, width=1600, height=800, mask = mask, background_color = 'white', max_font_size=600).generate(text=text).to_image()
		#wordcloud = WordCloud(mask=mask, font_path=fpath)
	else:
		pil_img = WordCloud(font_path=font_path, mask = mask, width=1600, height=800, background_color = 'white', max_font_size=600).generate(text=text).to_image()
		#wordcloud = WordCloud(font_path=fpath)
	#mask = np.array(Image.open("static/french_flag.png"))
	#pil_img = WordCloud(font_path=font_path, mask = mask, background_color = 'white', max_font_size=600).generate(text=text).to_image()
	#plt.figure(figsize=[7,7])
	#plt.imshow(wordcloud_spa.recolor(color_func=image_colors), interpolation="bilinear")
	#plt.axis("off")
	#wordcloud = WordCloud().generate(text)
	plt.imshow(pil_img, interpolation='bilinear')
	#plt.axis("off")
	plt.tight_layout(pad=0)
	#save it to a temporary buffer
	img = io.BytesIO()
	pil_img.save(img, "PNG")
	img.seek(0)
	img_64 = base64.b64encode(img.getvalue()).decode('utf-8')
	#data = base64.b64encode(img.getbuffer()).decode("ascii")
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
	ax.set_title(u'能量随时间的变化', fontproperties=font_name) 
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
	return result

def make_bargraph_matplot(keys, values):
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
	return img_64

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

''' @app.route("/youtube/correlation_matrix", methods=['GET'])
def correlation_matrix():
	keys = ['here', 'comes', 'a', 'wave', 'meant', 'to', 'wash', 'me', 'away.', '.', 'tide', 'that', 'is', "takin'", 'under.', 'swallowing', 'sand,', 'left', 'with', 'nothing', 'say.', 'my', 'voice', 'drowned', 'out', 'in', 'the', 'thunder.', 'but', 'i', "won't", 'cry.', 'and', 'start', 'crumble.', 'whenever', 'they', 'try.', 'shut', 'or', 'cut', 'down.', 'be', 'silenced.', 'you', "can't", 'keep', 'quiet.', 'tremble', 'try', 'it.', 'all', 'know', 'go', 'speechless.', "'cause", "i'll", 'breathe.', 'when', 'suffocate', 'me.', "don't", 'underestimate', 'written', 'stone', 'every', 'rule,', 'word.', 'centuries', 'old', 'unbending.', '"stay', 'your', 'place,', 'better', 'seen', 'not', 'heard".', 'well,', 'now', 'story', 'ending.', 'i.', 'cannot', 'so', 'come', 'on', 'speechless!.', 'let', 'storm', 'in.', 'broken.', 'no,', 'live', 'unspoken.', 'lock', 'this', 'cage.', 'just', 'lay', 'down', 'die.', 'will', 'take', 'these', 'broken', 'wings.', 'watch', 'burn', 'across', 'sky.', 'hear', 'echo', 'saying.', '"i', 'silenced".', 'though', 'wanna', 'see']
	values = [1, 1, 2, 1, 1, 9, 1, 11, 1, 39, 1, 5, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 1, 1, 23, 16, 1, 9, 2, 2, 1, 3, 2, 2, 1, 2, 2, 4, 2, 8, 2, 2, 2, 3, 7, 3, 4, 7, 7, 7, 6, 2, 2, 4, 2, 5, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
	bytes_obj = make_bargraph(keys, values)
	return send_file(bytes_obj, attachment_filename='plot.png', mimetype='image/png')
#https://python-sci-plotting.herokuapp.com/plots/breast_cancer_data/correlation_matrix
 '''

#Where I Upload Multiple Audio Files--only for wav files
def length_wav(fname): #finding the length of audio file
	import wave
	import contextlib
	with contextlib.closing(wave.open(fname,'r')) as f:
		frames = f.getnframes()
		rate = f.getframerate()
		duration = frames / float(rate)
	return duration

def length_mp3(fname):
	from mutagen.mp3 import MP3
	audio = MP3(fname)
	return audio.info.length

""" def stack_barchart():
	import json
	animals=['giraffes', 'orangutans', 'monkeys']
	import plotly.graph_objects as go
	fig = go.Figure(data=[
	go.Bar(name='SF Zoo', x=animals, y=[20, 14, 23]),
	go.Bar(name='LA Zoo', x=animals, y=[12, 18, 29])
	])
	# Change the bar mode
	fig.update_layout(barmode='stack')
	#fig.show()
	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) """

def create_plot(feature):
	import plotly
	import plotly.graph_objs as go
	import pandas as pd
	import numpy as np
	import json
	if feature == 'Bar':
		N = 40
		x = np.linspace(0, 1, N)
		y = np.random.randn(N)
		df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe
		data = [
			go.Bar(
				x=df['x'], # assign x as the dataframe column 'x'
				y=df['y']
			)
		]
		graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

	else:
		N = 1000
		random_x = np.random.randn(N)
		random_y = np.random.randn(N)

		# Create a trace
		data = [go.Scatter(
			x = random_x,
			y = random_y,
			mode = 'markers'
		)]
	graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON

@app.route('/bar', methods=['GET', 'POST'])
def change_features():
	feature = request.args['selected']
	graphJSON= create_plot(feature)
	return graphJSON

''' @app.route("/", )
def index():
	#bar = create_plot()
	feature = 'Bar'
	bar = create_plot(feature)
	return render_template("") '''


@app.route("/youtube", methods=['GET', 'POST'])
def youtube():
	feature = 'Bar'
	bar = create_plot(feature)
	import sys
	import requests
	import os 
	if request.method == 'POST':
		if request.form.get("Analyze") == 'Youtube':
			counter = 0 
			text = request.form['Text']
			id= text.split("=", 1)[0]
			if 'https://www.youtube.com/watch?v' not in id:
				flash('Not a YouTube link. Please upload a YouTube link')
				return redirect(request.url)
			elif text == '':
				flash('No selected YouTube link inputted ')
				return redirect(request.url)
			else: 
				youtube_id= text.split("=", 1)[1]
				#lyrics_path = lyrics_dir_path + 'LYRICS.txt' #str(counter).zfill(4) + ".txt"
				video_url = "https://www.youtube.com/watch?v=" + youtube_id
				Lyrics_URL = "http://video.google.com/timedtext?type=list&v=" + youtube_id #hSnB7zGW15M
				Lyrics = requests.get(Lyrics_URL)
				Lyrics = Lyrics.text
				if 'name=""' in Lyrics:
					lyrics_url = "http://video.google.com/timedtext?lang=en&v=" + youtube_id
					lyrics = requests.get(lyrics_url)
					texts= lyrics.text
					texts = cleanhtml(texts)
					#soup = BeautifulSoup(texts)
					#song_lyrics = soup.get_text()
					texts = deEmojify(texts)
					texts = texts.replace('&lt;font color=&quot;#FFFFFF&quot;&gt;&lt;i&gt;', " ")
					texts = texts.replace('&#39;', "'")
					texts = texts.replace('&quot;', '"')
					texts = texts.replace('&amp;#39;', "'")
					texts = texts.replace('&amp;quot;', '"')
					sentence = re.sub("(?!^)(?=\s\s)", ".", texts)
					sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
					sentences = sent_tokenizer.tokenize(sentence)
					sentences = [sent.capitalize() for sent in sentences]
					sentence = ' '.join(sentences)
					lexyranky = summarizing(sentence)
					sent = vader(sentence)
					cloud = get_wordcloud(sentence)
					data = word_counts(sentence.lower()) 
					keys = list(data)
					values= list(data.values())
					#Make Bar Graph 
					bar_graph= make_bargraph(keys, values)
					#lyrics_file = codecs.open(lyrics_path, mode='w+', encoding='utf-8')
					#lyrics_file.write(lyrics.text)
				elif 'name="en"' in Lyrics: 
					lyrics_url = "http://video.google.com/timedtext?name=en&lang=en&v=" + youtube_id
					lyrics = requests.get(lyrics_url)
					#print(type(lyrics)) #<class 'requests.models.Response'>
					texts= lyrics.text
					#print(type(texts)) #string 
					texts = cleanhtml(texts)
					#soup = BeautifulSoup(texts, features="lxml")
					#result1 = soup.find_all('text').text
					#print("TEXT STUFF: ", result1)
					#song_lyrics = soup.get_text() #only text stripping most HTML tags
					texts = deEmojify(texts)
					texts = texts.replace('&lt;font color=&quot;#FFFFFF&quot;&gt;&lt;i&gt;', " ")
					texts = texts.replace('&lt;/i&gt;&lt;/font&gt;', " ")
					texts = texts.replace('&amp;#39;', "'")
					texts = texts.replace('&amp;quot;', '"')
					marscapone = re.sub("(?!^)(?=\s\s)", ".", texts).lower()
					sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
					sentences = sent_tokenizer.tokenize(marscapone)
					sentences = [sent.capitalize() for sent in sentences]
					sentence = ' '.join(sentences)
					lexyranky = summarizing(sentence)
					sent = vader(sentence)
					cloud = get_wordcloud(sentence)
					data = word_counts(sentence.lower()) 
					keys = list(data)
					values= list(data.values())
					#Make Bar Graph 
					bar_graph= make_bargraph(keys, values)
					bar_graph_mat = make_bargraph_matplot(keys, values)
				else: 
					sounds_dir_path = "/music/sounds/"
					sound_path = sounds_dir_path + str(counter).zfill(4)
					os.system('youtube-dl --extract-audio --audio-format mp3 --prefer-ffmpeg -o' + os.getcwd() + sound_path + ".m4a " + video_url)
					sentence = "Could not transcribe! I have downloaded the YouTube link as an mp3 file in the /music/sounds folder. Please go to the 'Upload' link to upload the mp3 file and try to transcribe the audio there."
					counter += 1
					flash('File(s) successfully uploaded')
				return render_template("youtube.html", text= sentence, sent = sent, lexyranky = lexyranky, cloud =cloud, bar_graph = bar_graph, bar_graph_mat = bar_graph_mat)
		elif request.form.get("Analyze") == 'File':
			graphs = []
			graphs_mat = []
			clouds = []
			output = []
			output_punct = []
			filepaths = []
			if 'file[]' not in request.files:
				flash('No file part')
				return redirect(request.url)
			uploaded_files = request.files.getlist('file[]')
			for file in uploaded_files:
				if file and allowed_file(file.filename):
					filename = secure_filename(file.filename)
					filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
					filepaths.append(filepath)
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					#return redirect(request.url)
					name = '{}'.format(filename)
					storage_client = storage.Client()
					bucket = storage_client.get_bucket('awesome-bucketness')
					blob = storage.Blob(name, bucket)
					#blob = bucket.blob()
					blob.upload_from_filename(filepath)
					with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
						if filename.endswith(".mp3") and length_mp3(filepath) <=30:
							if 'fr' in filename:
								output.append(transcribe_audio_french(filepath))
							elif 'sp' in filename:
								output.append(transcribe_audio_naspanish(filepath))	
							elif 'ch' in filename:
								output.append(transcribe_audio_chinese(filepath))
							else:
								#print(filename) <FileStorage: 'transcript-sp.mp3' ('audio/mp3')>   <FileStorage: 'transcript.mp3' ('audio/mp3')>
								output.append(transcribe_audio(filepath))
						elif filename.endswith(".wav") and length_wav(filepath) <= 30:
							if 'fr' in filename:
								output.append(transcribe_audio_french(filepath))
							elif 'sp' in filename:
								output.append(transcribe_audio_naspanish(filepath))	
							elif 'ch' in filename:
								output.append(transcribe_audio_chinese(filepath))
							else:
								output.append(transcribe_audio(filepath))
								output_punct.append(transcribe_google_punct(filepath))
						elif filename.endswith(".mp3") and length_mp3(filepath) > 30:  
							if 'fr' in filename:
								output.append(transcribe_audio_french(filepath))
							elif 'sp' in filename:
								output.append(transcribe_audio_naspanish(filepath))	
							elif 'ch' in filename:
								output.append(transcribe_audio_chinese(filepath))
							else:
								output.append(sample_long_running_recognize("gs://awesome-bucketness/" + filename))
						elif filename.endswith(".wav") and length_wav(filepath) > 30:
							if 'fr' in filename:
								output.append(transcribe_audio_french(filepath))
							elif 'sp' in filename:
								output.append(transcribe_audio_naspanish(filepath))	
							elif 'ch' in filename:
								output.append(transcribe_audio_chinese(filepath))
							else:
								output.append(sample_long_running_recognize("gs://awesome-bucketness/" + filename))
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
						bar_graph_mat = make_bargraph_matplot(keys, values)
						graphs_mat.append(bar_graph_mat)
					flash('File(s) successfully uploaded')
				return render_template('youtube.html', plot = bar, filepaths = filepaths, output_punct= output_punct, graphs_mat = graphs_mat, lens = len(filepaths), len = len(uploaded_files), output=output, clouds = clouds, graphs = graphs)
		return ""

#------------------------------------------------------------------------------------------------------------------------------------, lexyranky = lexyranky, sent= sent

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