#Flask and Security Measures
from flask import (Blueprint, g, session, Flask, flash, make_response, render_template, redirect, request, url_for, send_file, send_from_directory, session, abort)
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
#from os import listdir #import lxml #import random; import json;

#Transcribing Files
from longaudio import silence_based_conversion, transcribe_audio, length
#imports the Google Cloud Client library
from google.cloud import storage; from googletrans import Translator #from two_speakers import sample_long_running_recognize_diarization
import uuid; import requests; #import sys; #import contextlib; import importlib #import wave; 

#Youtube Captions 
import html2text; import nltk; from os import path, system; from os import environ; from lxml import etree
# Making wordclouds and bargraphs
from io import BytesIO;import matplotlib.pyplot as plt; import numpy as np; import seaborn as sns; import base64
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator; from PIL import Image; 
#Chinese 
from matplotlib.figure import Figure; import jieba; from matplotlib.font_manager import FontProperties; from collections import Counter

import matplotlib
matplotlib.use('agg')
#For the different audio files
import re  #, string, unicodedata; import subprocess; import shlex; 
import urllib.request
from flask_wtf.csrf import CSRFProtect; from flask_wtf.csrf import CSRFError 

app = Flask(__name__)
app.secret_key = "dzt+QGupE5lVkNrPl5cPu6ICErr9pnPzV0wMCKBTcvA="  
#used by Flask and extension to keep data safe. Set as a convient value during development, but should be overriden with a random value when deploying.
csrf = CSRFProtect(app)

app = Flask(__name__)
app.secret_key = "dzt+QGupE5lVkNrPl5cPu6ICErr9pnPzV0wMCKBTcvA="
#app.config['TEMPLATES_AUTO_RELOAD'] = True

bootstrap = Bootstrap(app)

font_path = 'fonts/STFangSong.ttf' #chinese = FontProperties(fname=r'/Library/Fonts/Microsoft/SimHei.ttf', size=20) 
font_name= FontProperties('Heiti TC')

#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['wav', 'flac', 'mp3', 'm4a', 'ogg'])

environ["GOOGLE_APPLICATION_CREDENTIALS"]="My Project 52130-da00a565db68.json"

@app.route("/")
def home():
	return render_template("home.html")

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
	return render_template('csrf_error.html', reason=e.description), 400
		
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
	return make_response('All good')


@app.route("/start")
def start():
	response = make_response(redirect('/'))
	session_id = uuid.uuid4().hex
	response.set_cookie('session_id', session_id)
	return response

userdict_list = ['阿Ｑ', '孔乙己', '单四嫂子']

def jieba_processing_txt(text):
	#jieba.enable_parallel(4) # Setting up parallel processes :4 ,but unable to run on Windows
	for word in userdict_list:
		jieba.add_word(word)
	mywordlist = []
	seg_list = jieba.cut(text, cut_all=False)
	liststr = "/ ".join(seg_list)

	for myword in liststr.split('/'):
		if len(myword.strip()) > 1:
			mywordlist.append(myword)
	return ' '.join(mywordlist)

@app.route('/youtube', methods=['GET', 'POST'])
def uploading():
	#global sites
	sites = {'English': 'en-US', 'French': 'fr-FR', 'Spanish': 'es-MX', 'Chinese': 'zh-CN', 'Tagalog':'tl-PH', }
	return render_template('uploading.html', sites=sites) 

@app.route('/result', methods=['POST'])
def resultss():
	global langue#; global clouds; global filepaths; global output; global uploaded_files # global graphs; global result ; global cloud; global filepath; 
	graphs = []; clouds = []; output = [] #filepaths = []; clouds1 = []; clouds2 = []; clouds3 = []#masks = ['American Flag', 'French Flag', 'Spanish Flag', 'Chinese Flag']
	langue = str(request.form.get('site'))	
	if request.form.get("Analyze") == 'File': #pdb.set_trace()
		if 'file[]' not in request.files:
			flash('No file part')
			return redirect(request.url)
		uploaded_files = request.files.getlist('file[]') #print(simplejson.dumps({"files": [result.get_file()]}))
		for file in uploaded_files: #<FileStorage: 'female.wav' ('audio/wav')>
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				name = '{}'.format(filename)
				storage_client = storage.Client()
				bucket = storage_client.get_bucket('awesome-bucketness')
				blob = storage.Blob(name, bucket)
				content = 'audio/' + re.split('\.',name)[1]
				file.seek(0)
				blob.upload_from_string(file.read(), content_type=content)
				if length(name) <=30 or length(name) <= 000030.00: 
					file.seek(0)
					output.append(transcribe_audio(file.read(), name, langue))
				else:
					file.seek(0)
					output.append(silence_based_conversion(file.read(), name, langue))
		for i in range(0, len(uploaded_files)):
			#filename = secure_filename(file.filename)
			if langue =='zh-CN': #in filename:
				words = jieba_processing_txt(output[i]) 
				data = Counter(output[i])
			else:
				words = output[i] 
				data = word_counts(output[i].lower()) 
			cloud = get_wordcloud(words)
			clouds.append(cloud) #clouds1.append(get_wordcloud(output[i], mask = "static/img/french_flag.png")) #clouds2.append(get_wordcloud(output[i], mask = "static/img/spain_flag.png")) #clouds3.append(get_wordcloud(output[i], mask = "static/img/china_flag.jpg"))
			keys = list(data)
			values= list(data.values())
			#Make Bar Graph 
			bar_graph= make_bargraph(keys, values)
			graphs.append(bar_graph)  
		#flash('File(s) successfully uploaded')
		return render_template('result.html', filepaths = file.read() , clouds = clouds, graphs = graphs, len = len(uploaded_files), output=output)  #, lens = len(filepaths), clouds1 = clouds1 , clouds2= clouds2 , clouds3=clouds3, masks= masks, length_mask = len(masks), 

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_wordcloud(text):
 	#text = text.decode("utf-8")
	if langue =='zh-CN':
		pil_img = WordCloud(font_path=font_path, background_color="white", max_words=2000, max_font_size=100, random_state=42, width=1000, height=860, margin=2,).generate(jieba_processing_txt(text))
	else:
		pil_img = WordCloud(width=1600, height=800, scale = 20, background_color = 'white', mode="RGBA", max_font_size=600).generate(text=text) #mask = mask,
	img = BytesIO() #mask = np.array(Image.open(mask).convert('RGB')) #image_colors = ImageColorGenerator(mask)
	plt.figure(figsize=[7,7]) 
	pil_img = pil_img.to_image() 
	plt.axis("off") #no axis?     
	plt.tight_layout(pad=0)
	img = BytesIO() 	#save it to a temporary buffer
	pil_img.save(img, "PNG") #save this byte to a PNG
	img.seek(0)
	img_64 = base64.b64encode(img.getvalue()).decode('utf-8')
	return img_64

def make_bargraph(keys, values):
	#fig= Figure() #ax = fig.subplots()
	if langue == 'zh-CN':
		fig, ax = plt.subplots(figsize=(11,9)); width = 0.60  
		ax.bar(keys, values, width) #Make bar graph
		ax.set_title(u'说的字数', fontproperties=font_name) 		# Set common labels
		ax.set_xlabel(u'次数',fontproperties=font_name)
		ax.set_ylabel(u'字', fontproperties=font_name)
		ax.set_xticks(keys)
		for label in ax.xaxis.get_majorticklabels():
			label.set(fontproperties=font_name)
		#set parameters for tick labels
		ax.tick_params(axis='x', which='major', labelsize=5, grid_linewidth = 100) #plt.xticks(keys, fontproperties=chinese) 
	else:
		sns.set_style("white")
		f, ax = plt.subplots(figsize=(11, 9)) # this creates a figure 11 inch wide, 9 inch high
		ax = sns.barplot(values, keys)
		ax.set(xlabel="Number of times", ylabel='Words')
		fig = ax.get_figure()
		#bytes_image = io.BytesIO()
	bytes_image = BytesIO()
	fig.savefig(bytes_image, format="png")
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
	global youtube_id; global output; 
	#global bar_graph; global cloud; global filepath; 
	#global video_title; video_title = [] 
	#clouds = []; clouds1 = []; clouds2 = []; clouds3 = []; graphs= []; #masks = ['American Flag', 'French Flag', 'Spanish Flag', 'Chinese Flag']
	if request.form.get("Analyze") == 'Youtube':
		text = request.form['Text']
		youtube_id= text.split("=", 1)[1]
		video_url = "https://www.youtube.com/watch?v=" + youtube_id
		youtube = etree.HTML(urllib.request.urlopen(video_url).read()) #enter your youtube url here
		video_title = youtube.xpath("//span[@id='eow-title']/@title") #get xpath using firepath firefox addon and gets NAME OF SONG
		#''.join(video_title)
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

if __name__ == "__main__":
	app.run(debug=True)
