<img alt="https://img.shields.io/pypi/pyversions/requests.svg" src="https://img.shields.io/pypi/pyversions/requests.svg">



Run python. if you have Python3, then you can pip install. If you are not in Python3, run with pip3 install <package name>

  
Run the following on your terminal: 
```
pip install flask
pip install SpeechRecognition 
pip install sounddevice 
pip install pydub
pip install soundfile
pip install google-cloud-storage 
pip install googletrans #this is used to translate the webpage
pip install sumy 
```
<div class="bg-green-light mb-2"> in the document, it says speech_recognition. That is not the package name!</div>
<div class="bg-yellow mb-2">helps to record audio</div>
this is used to upload the files that user provides in the 'Upload' or 'Record' section
this is used to translate the webpage
this is used to use lexrank
<hr>

# Running Locally #

**Set up virtual environment (This is only for MAC) ** 
```
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```

**Create a Cloud Storage bucket. It is recommended that you name it the same as your project ID: ( I named it awesome bucketness, so whatever)**
```
gsutil mb gs://${PROJECT_ID}
```

**Set the environmental variable CLOUD_STORAGE_BUCKET:**
```
export CLOUD_STORAGE_BUCKET=${PROJECT_ID}
```

**Then in the virtual environment (you will see <env> to the left of your terminal), run these commands:**
```
export FLASK_ENV="development"
main python.py
```
