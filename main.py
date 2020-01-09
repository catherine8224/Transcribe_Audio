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

from transcribe import transcribe_audio
#from shortaudio import sample_recognize
from word_cloud import wordcloud_something
#imports the Google Cloud Client library
from google.cloud import storage
import uuid
from googletrans import Translator

import numpy as np
#import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
from os import path
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import base64

import matplotlib
matplotlib.use('agg')
from flask_mail import Message, Mail

UPLOAD_FOLDER = '/Users/catherineng/Desktop/Python Projects/Hunter Codefest/app/templates'

app = Flask(__name__)

#CLOUD_STORAGE_BUCKET = os.environ['GCP_PROJECT']

app.secret_key = "secret key" #used by Flask and extension to keep data safe. Set as a convient value during development, but should be overriden with a random value when deploying.
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #where we will store the uploaded files
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
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

def get_wordcloud(text):
	#text = ('conscious of its spiritual and moral Heritage the union is founded on the indivisible Universal values of human dignity Freedom equality and solidarity it is based on the principles of democracy and the rule of law it places the individual at the heart of its activities by establishing the citizenship of the union and by creating an area of Freedom security and justice')
	pil_img = WordCloud(background_color ='white').generate(text=text).to_image()
	#wordcloud = WordCloud().generate(text)
	#plt.imshow(wordcloud, interpolation='bilinear')
	#plt.axis("off")
	#save it to a temporary buffer
	img = io.BytesIO()
	pil_img.save(img, "PNG")
	#wordcloud.to_image().save(img, 'PNG')
	img.seek(0)
	img_64 = base64.b64encode(img.getvalue()).decode()
	#data = base64.b64encode(img.getbuffer()).decode("ascii")
	return img_64
	#return f"<img src='data:image/png;base64,{data}'/>"
	#return send_file(img, mimetype='image/png')

def word_counts(str): 
	counts = dict()
	words = str.split()

	for word in words:
		if word in counts:
			counts[word] += 1
		else:
			counts[word] = 1
	return counts

def make_bargraph(keys, values):
	fig= Figure()
	ax = fig.subplots()
	width = 0.75
	#ax.plot([1,2])
	#fig, ax = plt.subplots()
	ax. barh(keys, values, width, color = "blue")
	# Set common labels
	ax.set_title('Audio-Number of times words were said')
	ax.set_xlabel('Number of times')
	ax.set_ylabel('Words')
	#fig = plt.bar(*zip(*data.items()), label = "Word counts")
	#plt.xticks(rotation='vertical')
	#plt.xlabel('Words')
	#plt.tight_layout() 
	buf = BytesIO()
	fig.savefig(buf, format="png")
	#wordcloud.to_image().save(img, 'PNG')
	#img.seek(0)
	img_64 = base64.b64encode(buf.getbuffer()).decode('ascii')
	#data = base64.b64encode(img.getbuffer()).decode("ascii")
	return img_64

#Where I Upload Multiple Audio Files
@app.route('/uploads_form')
def uploads_form():
	return render_template('uploads.html')

@app.route('/uploads_form', methods=['GET', 'POST'])
def uploads_file():
	#filenames= []
	#if request.method == 'POST':
		# check if the post request has the files part
	#	if 'files[]' not in request.files:
	#		flash('No file part')
	#		return redirect(request.url)
	uploaded_files = request.files.getlist('file[]')
	for file in uploaded_files:
	#for file in files:
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			#filenames.append(filename) 
			name = '{}'.format(filename)
			storage_client = storage.Client()
			bucket = storage_client.get_bucket('awesome-bucketness')
			blob = storage.Blob(name, bucket)
			blob.upload_from_filename(filepath)
			with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
				output = transcribe_audio(filename)
			#cloud = get_wordcloud(output)
			#data = word_counts(output.lower())
			#keys = list(data)
			#values= list(data.values())
			#Make Bar Graph 
			#bar_graph= make_bargraph(keys, values)
		#flash('File(s) successfully uploaded')
		return render_template("uploads.html", output = output)

@app.route('/uploads_form/<filename>')
def uploaded_files(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],
							   filename)


#Where I Upload an Audio File
@app.route('/upload_form')
def upload_form():
	return render_template('upload.html')

@app.route('/upload_form', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('File successfully uploaded')
			#return redirect(request.url)
			name = '{}'.format(filename)
			storage_client = storage.Client()
			bucket = storage_client.get_bucket('awesome-bucketness')
			blob = storage.Blob(name, bucket)
			#blob = bucket.blob()
			blob.upload_from_filename(filepath)
			#return sample_recognize('gs://awesome-bucketness/transcript.mp3')
			#with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as p:
			#    oput = sample_recognize("gs://awesome-bucketness/" + name)
			#    with open('transcribe.txt', 'w') as f:
			#        f.write(str(oput))
			#return render_template('upload.html'), oput
			with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
				print(filename)
				output = transcribe_audio(filename)
			cloud = get_wordcloud(output)
			#translator = Translator() # Create object of Translator
			#translated = translator.translate(output, src='en', dest='ko') # Pass both source and destination
			#kor = " KOREAN \n" + translated.text
			#translated = translator.translate(output, src='en', dest='fil')
			#fil = " TAGALOG \n" + translated.text
			data = word_counts(output.lower())
			keys = list(data)
			values= list(data.values())
			#Make Bar Graph 
			bar_graph= make_bargraph(keys, values)
			return render_template("upload.html", output = output, article=cloud, graph = bar_graph)
		else:
			flash('ERROR: Allowed filetypes are mp3, flac, wav')
			return redirect(request.url)
	return "Hello World"

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],
							   filename)

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
#@app.route('/background_process_test')
#def background_process_test():
#    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
#                output = transcribe_audio(f)
#            with open('transcribe.txt', 'w') as f:
#                f.write(str(output))
#            return output

# @app.route("/record_form/<path>")
# def DownloadLogFile (path = None):
#     if path is None:
#         self.Error(400)
#     try:
#         return send_file(path, as_attachment=True)
#         output = transcribe_audio(path)
#         with open('transcribe.txt', 'w') as f:
#             f.write(str(output))
#         return output
#     except Exception as e:
#         self.log.exception(e)
#         self.Error(400)

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
#                 output = transcribe_audio(f)
#             with open('transcribe.txt', 'w') as f:
#                 f.write(str(output))
#             return redirect(url_for('uploaded_file',
#                                     filename=filename)), output
#@app.route('/uploads/<filename>', methods=['GET'])
#def script_output():
#    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
#        output= transcribe_audio(f)
#    return output


if __name__ == "__main__":
	app.run(debug=True)
  #We made two new changes