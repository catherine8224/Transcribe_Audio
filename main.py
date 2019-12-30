import os
from os import listdir
import urllib.request
from app import app
from flask import Flask, flash, render_template, redirect, request, url_for 
from werkzeug.utils import secure_filename 

from flask_wtf.csrf import CsrfProtect
app = Flask(__name__)
app.secret_key = 'very secret'
CsrfProtect(app)


from transcribe import transcribe_audio
from google.cloud import storage

UPLOAD_FOLDER = '/Users/catherineng/'

app = Flask(__name__)

#CLOUD_STORAGE_BUCKET = os.environ['GCP_PROJECT']

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['wav', 'flac', 'mp3', 'm4a'])

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/")
def home():
    session_id = request.cookies.get('session_id')
    if session_id:
        all_done = request.cookies.get('all_done')
        if all_done:
            return render_template("thanks.html")
        #else:
        #    return render_template("record.html")
    else:
        return render_template("template.html")
    #return render_template("home.html")
    

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_form')
def upload_form():
    return render_template('upload.html')

@app.route('/record_form')
def record_form():
    return render_template('record.html')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
                output = transcribe_audio(f)
            with open('transcribe.txt', 'w') as f:
                f.write(str(output))
            return redirect(url_for('uploaded_file',
                                    filename=filename)), output


from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

#@app.route('/uploads/<filename>', methods=['GET'])
#def script_output():
#    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
#        output= transcribe_audio(f)
#    return output


if __name__ == "__main__":
    app.run(debug=True)
  #We made two new changes