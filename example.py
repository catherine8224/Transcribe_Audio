import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import base64
from io import BytesIO
import numpy as np

def word_counts(str): 
	counts = dict()
	words = str.split()

	for word in words:
		if word in counts:
			counts[word] += 1
		else:
			counts[word] = 1
	return counts

transcription = 'conscious of its spiritual and moral Heritage the union is founded on the indivisible Universal values of human dignity Freedom equality and solidarity it is based on the principles of democracy and the rule of law it places the individual at the heart of its activities by establishing the citizenship of the union and by creating an area of Freedom security and justice'
data = word_counts(transcription.lower())
keys = list(data)
values= list(data.values())
#print(list(data))
#print(list(data.values()))

x = [u'INFO', u'CUISINE', u'TYPE_OF_PLACE', u'DRINK', u'PLACE', u'MEAL_TIME', u'DISH', u'NEIGHBOURHOOD']
y = [160, 167, 137, 18, 120, 36, 155, 130]

def make_bargraph(data):
	fig= Figure()
	ax = fig.subplots()
	width = 0.75
	ax.plot([1,2])
	#fig, ax = plt.subplots()
	ax. barh(keys, values, width, color = "blue")
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

#print(make_bargraph(data))



 @app.route('/uploads_form')
def uploads_form():
		return render_template('youtube.html')

@app.route('/uploads_form', methods=['GET', 'POST'])
def uploads_file():
	graphs = []
	clouds = []
	output = []
	filepaths = []
	if request.method == 'POST':
		# check if the post request has the files part
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
				#print(filepath)
				name = '{}'.format(filename)
				storage_client = storage.Client()
				bucket = storage_client.get_bucket('awesome-bucketness')
				blob = storage.Blob(name, bucket)
				#blob = bucket.blob()
				blob.upload_from_filename(filepath)
				if length(filepath) <= 30:
					with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
						if 'fr' in filename:
							#print(filename) <FileStorage: 'transcript-sp.mp3' ('audio/mp3')>   <FileStorage: 'transcript.mp3' ('audio/mp3')>
							output.append(transcribe_audio_french(filepath))
						elif 'sp' in filename:
							output.append(transcribe_audio_naspanish(filepath))	
						elif 'ch' in filename:
							output.append(transcribe_audio_chinese(filepath))
						else:
							#print(filename) <FileStorage: 'transcript-sp.mp3' ('audio/mp3')>   <FileStorage: 'transcript.mp3' ('audio/mp3')>
							output.append(transcribe_audio(filepath))
				elif length(filepath) > 30: 
					with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
						if 'fr' in filename:
							#print(filename) <FileStorage: 'transcript-sp.mp3' ('audio/mp3')>   <FileStorage: 'transcript.mp3' ('audio/mp3')>
							output.append(transcribe_audio_french(filepath))
						elif 'sp' in filename:
							output.append(transcribe_audio_naspanish(filepath))	
						elif 'ch' in filename:
							output.append(transcribe_audio_chinese(filepath))
						else:
							#print(filename) <FileStorage: 'transcript-sp.mp3' ('audio/mp3')>   <FileStorage: 'transcript.mp3' ('audio/mp3')>
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
		flash('File(s) successfully uploaded')
		return render_template('youtube.html', filepaths = filepaths, lens = len(filepaths), len = len(uploaded_files), output=output, article = clouds, graphs = graphs, lexyranky = lexyranky, sent= sent)
	return ""
 '''
#@app.route('/upload_forms/<path:filename>')
#def uploaded_files(filename):
#	return send_from_directory(app.config['UPLOAD_FOLDER'],
#							   filename)







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

fname = "/Users/catherineng/Desktop/Python_Projects/huntercodefest/transcript-fr.mp3"

def length_mp3(fname):
	from mutagen.mp3 import MP3
	audio = MP3(fname)
	return audio.info.length

#print(length_mp3(fname))


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
		print("x: " + x)
		print("y: " + y)
		print(data)
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

feature = "Bar"
create_plot()