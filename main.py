import os
from os import listdir
from flask import (Blueprint, g, session, Flask, flash, make_response, render_template, redirect, request, url_for, send_file, send_from_directory, session, abort)
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
#from forms import ContactForm
from transcribe import transcribe_audio#, transcribe_audio_french, transcribe_audio_naspanish, transcribe_audio_chinese, transcribe_google_punct
#, get_duration, get_duration_channels
#imports the Google Cloud Client library
from google.cloud import storage
import uuid; import simplejson; import requests; import sys; import io; import wave; import contextlib	
import importlib
#from googletrans import Translator
#import plotly
#import plotly.graph_objs as go
#import pandas as pd
#from matplotlib.font_manager import FontProperties 

#Youtube Captions 
import html2text; import nltk; from os import path; import matplotlib.pyplot as plt; import numpy as np; import seaborn as sns;
#from matplotlib.figure import Figure
import base64

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator; from PIL import Image; import jieba
import matplotlib
matplotlib.use('agg')
#from flask_mail import Message, Mail
import random; import re, string, unicodedata; from flask_bootstrap import Bootstrap
import subprocess; import shlex; import json; import pdb
#import lxml
from lxml import etree; import urllib.request

from io import BytesIO; import io; from flask_wtf.csrf import CSRFProtect; from flask_wtf.csrf import CSRFError 

app = Flask(__name__)
app.secret_key = "dzt+QGupE5lVkNrPl5cPu6ICErr9pnPzV0wMCKBTcvA="  #used by Flask and extension to keep data safe. Set as a convient value during development, but should be overriden with a random value when deploying.
csrf = CSRFProtect(app)


app = Flask(__name__)
app.secret_key = "dzt+QGupE5lVkNrPl5cPu6ICErr9pnPzV0wMCKBTcvA="
app.config['UPLOAD_FOLDER'] = 'static/uploaded_files' #where we will store the uploaded files
#app.config['TEMPLATES_AUTO_RELOAD'] = True
#from two_speakers import sample_long_running_recognize_diarization

bootstrap = Bootstrap(app)

#font_path = 'fonts/STFangSong.ttf'
#chinese = FontProperties(fname=r'/Library/Fonts/Microsoft/SimHei.ttf', size=20) 
#font_name= FontProperties('Heiti TC')

#UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads/..')

#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
""" mail = Mail()

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'cathygreat828@gmail.com'
app.config["MAIL_PASSWORD"] = 'WenTiDoc456'
 
mail.init_app(app) """

ALLOWED_EXTENSIONS = set(['wav', 'flac', 'mp3', 'm4a', 'ogg'])

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/catherineng/Downloads/My Project 52130-da00a565db68.json"

@app.route("/")
def home():
	return render_template("home.html")

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
	return render_template('csrf_error.html', reason=e.description), 400

'''
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
		
		
@app.route('/record_form')
def record_form():
	return render_template('record.html')

@app.route('/record_form', methods=['POST'])
def upload():
	#session_id = request.cookies.get('session_id')
	word= request.args.get('word')
	audio_data = request.data
	filename = word + '.ogg'
	secure_name= secure_filename(filename)
	gcs = storage.Client()
	bucket = gcs.get_bucket('awesome-bucketness')
	blob = storage.Blob(secure_name, bucket)
	blob.upload_from_string(audio_data, content_type='audio/ogg')
	return make_response('All good')'''


@app.route("/start")
def start():
	response = make_response(redirect('/'))
	session_id = uuid.uuid4().hex
	response.set_cookie('session_id', session_id)
	return response

@app.route('/youtube', methods=['GET', 'POST'])
def uploading():
	global sites
	sites = {'English': 'en-US', 'French': 'fr-FR', 'Spanish': 'es-MX'}
	return render_template('uploading.html', sites=sites) 

@app.route('/result', methods=['POST'])
def resultss():
	global filepath; global graphs ; global clouds; global filepaths; global output; global cloud ; global result; global uploaded_files
	output = []; filepaths = []; graphs = []; clouds = []#; clouds1 = []; clouds2 = []; clouds3 = []#masks = ['American Flag', 'French Flag', 'Spanish Flag', 'Chinese Flag']
	langue = str(request.form.get('site'))	
	#speakers = str(request.form["num"])  # gather = str(gather)
	if request.form.get("Analyze") == 'File':
		#pdb.set_trace()
		if 'file[]' not in request.files:
			flash('No file part')
			return redirect(request.url)
		uploaded_files = request.files.getlist('file[]')
		#print(simplejson.dumps({"files": [result.get_file()]}))
		for file in uploaded_files:
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				#print("File Name: ", filename)
				filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
				#print("FILE PATH: ", filepath)
				filepaths.append(filepath)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				name = '{}'.format(filename)
				storage_client = storage.Client()
				bucket = storage_client.get_bucket('awesome-bucketness')
				blob = storage.Blob(name, bucket)
				#blob = bucket.blob()
				blob.upload_from_filename(filepath)
				with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
					if length(filepath) <=30 or length(filepath) <= 000030.00: 
						output.append(transcribe_audio(filepath, langue))
					else:
						sentence = "file size too big"
						#return render_template("result.html", sentence=sentence) 
					print("OUTPUT:", output)
		for i in range(0, len(uploaded_files)):
			filename = secure_filename(file.filename)
			cloud = get_wordcloud(output[i])
			clouds.append(cloud) #clouds1.append(get_wordcloud(output[i], mask = "static/img/french_flag.png")) #clouds2.append(get_wordcloud(output[i], mask = "static/img/spain_flag.png")) #clouds3.append(get_wordcloud(output[i], mask = "static/img/china_flag.jpg"))
			data = word_counts(output[i].lower()) 
			keys = list(data)
			values= list(data.values())
			#Make Bar Graph 
			bar_graph= make_bargraph(keys, values)
			graphs.append(bar_graph)  
		flash('File(s) successfully uploaded')
		return render_template('result.html', clouds = clouds, filepaths = filepaths, graphs = graphs, len = len(uploaded_files), output=output)  #lens = len(filepaths), clouds1 = clouds1 , clouds2= clouds2 , clouds3=clouds3, masks= masks, length_mask = len(masks), 
	#return ''

def length(fname): #finding the length of audio file
	if fname.endswith(".wav") or fname.endswith(".WAV"):
		with contextlib.closing(wave.open(fname,'r')) as f:
			frames = f.getnframes()
			rate = f.getframerate()
			duration = frames / float(rate)
		return duration
	else:
		extension = re.split('\.', fname)[1]  #flac, mp3
		mymodule = importlib.import_module("mutagen." + extension)
		#from mutagen.mp3 import MP3
		if fname.endswith(".mp3"):
			audio = mymodule.MP3(fname)
		elif fname.endswith(".flac"):
			audio = mymodule.FLACK(fname)
		elif fname.endswith(".m4a"):
			audio = mymodule.M4A(fname)
		if audio is None: 
			#var = os.system("ffmpeg -i /Users/catherineng/Downloads/0aeaedfc-b0ee-4ad1-a6b7-85ed8e588400.ogg -loglevel quiet -stats -f null - 2>&1 | awk '{print $2}' | sed s/://g | sed s/[a-z]//g | sed s/=//g")
			var = os.system("ffmpeg -i " + fname + " -loglevel quiet -stats -f null - 2>&1 | awk '{print $2}' | sed s/://g | sed s/[a-z]//g | sed s/=//g")
			return var
		else: 
			return audio.info.length
	# if fname.endswith(".ogg"):
	# 	import mutagen
	# 	audio = mutagen.File(fname)
	# 	if audio is None: 
	# 		var = os.system("ffmpeg -i " + fname + " -loglevel quiet -stats -f null - 2>&1 | awk '{print $2}' | sed s/://g | sed s/[a-z]//g | sed s/=//g")
	# 		return var
	# 	else: 
	# 		return audio.info.length

# @app.route("/start")
# def start():
# 	response = make_response(redirect('/'))
# 	session_id = uuid.uuid4().hex
# 	response.set_cookie('session_id', session_id)
# 	return response

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_wordcloud(text, mask = "static/img/american_flag.png"):
 	#text = text.decode("utf-8")
	mask = np.array(Image.open(mask).convert('RGB'))
	pil_img = WordCloud(width=1600, height=800, mask = mask, scale = 20, background_color = 'white', mode="RGBA", max_font_size=600).generate(text=text)
	image_colors = ImageColorGenerator(mask)
	plt.figure(figsize=[7,7])
	plt.imshow(pil_img.recolor(color_func=image_colors), interpolation='bilinear')
	pil_img = pil_img.to_image()
	plt.axis("off")
	#plt.imshow(pil_img, interpolation='bilinear')
	plt.tight_layout(pad=0)
 	#save it to a temporary buffer
	img = io.BytesIO()
	pil_img.save(img, "PNG")
	img.seek(0)
	img_64 = base64.b64encode(img.getvalue()).decode('utf-8')
	return img_64

def make_bargraph(keys, values):
	#fig= Figure()
	#ax = fig.subplots()
	sns.set_style("white")
	f, ax = plt.subplots(figsize=(11, 9)) # this creates a figure 11 inch wide, 9 inch high
	ax = sns.barplot(values, keys)
	ax.set(xlabel="Number of times", ylabel='Words')
	fig = ax.get_figure()
	bytes_image = io.BytesIO()
	plt.savefig(bytes_image, format="png")
	bytes_image.seek(0)
	figdata_png = base64.b64encode(bytes_image.getvalue())
	result = str(figdata_png)[2:-1]
	#img_64 = base64.b64encode(buf.getbuffer()).decode('ascii')
	return result

def word_counts(str): 
	counts = dict()
	words = str.split()
	for word in words:
		if word in counts:
			counts[word] += 1
		else:
			counts[word] = 1
	return counts

def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext    	

def cleaning_lyrics(youtube_id):
	global sentence
	Lyrics = requests.get("http://video.google.com/timedtext?type=list&v=" + youtube_id).text
	result = re.findall(r'name="[A-Z|a-z]+"', Lyrics) #name="en"
	if not result:
		lyrics_url = "http://video.google.com/timedtext?" + "&lang=en&v=" + youtube_id #only get first language from result
	else:
		lyrics_url = "http://video.google.com/timedtext?" + result[0].replace('"', '') + "&lang=en&v=" + youtube_id #only get first language from result
	lyrics = requests.get(lyrics_url).text
	html = html2text.HTML2Text()
	unicodeparser = lyrics.encode('ascii', 'ignore').decode('utf-8') #deemojify the music notes
	texts = html.handle(unicodeparser).replace('\n', ' ')
	texts = cleanhtml(texts)
	marscapone = re.sub("(?!^)(?=\s\s)", ".", texts).lower()
	sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	sentences = sent_tokenizer.tokenize(marscapone)
	sentences = [sent.capitalize() for sent in sentences]
	sentence = ' '.join(sentences)
	return sentence

@app.route("/result_yt", methods=['GET', 'POST'])
def youtube():
	global youtube_id  
	global output
	global video_title
	global filepath
	global bar_graph
	global cloud
	video_title = []
	#clouds = []; clouds1 = []; clouds2 = []; clouds3 = []; graphs= []; #masks = ['American Flag', 'French Flag', 'Spanish Flag', 'Chinese Flag']
	if request.form.get("Analyze") == 'Youtube':
		text = request.form['Text']
		youtube_id= text.split("=", 1)[1]
		video_url = "https://www.youtube.com/watch?v=" + youtube_id
		youtube = etree.HTML(urllib.request.urlopen(video_url).read()) #enter your youtube url here
		video_title = youtube.xpath("//span[@id='eow-title']/@title") #get xpath using firepath firefox addon and gets NAME OF SONG
		#''.join(video_title) #Lyrics_URL = 
		#Lyrics = requests.get("http://video.google.com/timedtext?type=list&v=" + youtube_id).text
		#if 'name=""' in Lyrics or 'name="en"' in Lyrics:
		sentences = cleaning_lyrics(youtube_id)
		#sentences.append(cleaned)
		#clouds.append(get_wordcloud(sentences))
		clouds = get_wordcloud(sentences)
		data = word_counts(sentences.lower()) 
		keys = list(data)
		values= list(data.values())
		#Make Bar Graph 
		graphs= make_bargraph(keys, values)
		#graphs.append(bar_graph)
		return render_template("result_yt.html", sentences = sentences, video_title = video_title, clouds = clouds, graphs=graphs) #bar_graph = bar_graph, len = len(bloggy), length_mask = len(masks), masks = masks,
	else:
		sentence = "Could not transcribe! Please download the YouTube link as an mp3 file. Please go to the 'Upload' link to upload the mp3 file and try to transcribe the audio there."
		return render_template("result_yt.html", sentence=sentence) #filepath= filepath,
	#return ''


if __name__ == "__main__":
	app.run(debug=True)

# if 'ch' in filename:
# 	words = jieba_processing_txt(output[i])
# 	cloud = get_wordcloud_ch(words)
# 	clouds.append(cloud)
# 	data = Counter(output[i])
# 	keys = list(data)
# 	values= list(data.values())
# 	#Make Bar Graph 
# 	bar_graph= make_bar_ch(keys, values) 
# 	graphs.append(bar_graph)	
#else:
"""userdict_list = ['阿Ｑ', '孔乙己', '单四嫂子']

def jieba_processing_txt(text):
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
	img.seek(0)
	img_64 = base64.b64encode(img.getvalue()).decode('utf-8')
	#data = base64.b64encode(img.getbuffer()).decode("ascii")
	return img_64
"""
"""
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
"""

"""
#CREATE DOUBLE BARPLOT AND REGULAR BAR PLOT
def create_plot(feature):
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
				name='Second File Upload', 
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
"""

"""
def sample_long_running_recognize(storage_uri):
	from google.cloud import speech_v1
	#from google.cloud import speech_v1p1beta1
	from google.cloud.speech_v1 import enums
	#from google.cloud import speech

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
		alternatives = alternative.transcript
		#print(type(alternatives))
		stored_data.append(alternatives)
		data = ' '.join(stored_data[::2])
	return data
"""
'''@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
							   'favicon.ico', mimetype='image/vnd.microsoft.icon') 
@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/thanks")
def thanks():
	return render_template("thanks.html")
'''