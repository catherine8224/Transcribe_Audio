#Generating a summary of a text	
#SumBasic (word-based) (do stop words and stemming before doing this)
#Graph-based Methods: TextRank (relationship-based), 
# Latent Semantic Analysis (semantic-based)
# Lex-Rank: unsupervised approach to text summarization based on graph-based centrality scoring of sentences.

# Load Packages
import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def summarizing(document):
    #For Strings
    parser = PlaintextParser.from_string(document,Tokenizer("english"))
    #For files
    #parser = PlaintextParser.from_file(file, Tokenizer("english"))

    # Using LexRank
    summarizer = LexRankSummarizer()
    #Summarize the document with 2 sentences
    summary = summarizer(parser.document, 2)
    for sentence in summary:
        return(sentence)

from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

def vader(document):
    message_text = document
    # Calling the polarity_scores method on sid and passing in the message_text outputs a dictionary with negative, neutral, positive, and compound scores for the input text
    scores = sid.polarity_scores(message_text)

    # Here we loop through the keys contained in scores (pos, neu, neg, and compound scores) and print the key-value pairs on the screen
    for key in sorted(scores):
        result = '{0}: {1}, '.format(key, scores[key]), end=''
    return result





for file in uploaded_files:
    			#if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			#filenames.append(filename) 
			name = '{}'.format(filename)
			storage_client = storage.Client()
			bucket = storage_client.get_bucket('awesome-bucketness')
			blob = storage.Blob(name, bucket)
			blob.upload_from_filename(filepath)
			#with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
			output = transcribe_audio(filename)
			return render_template("uploads.html", output = output)
		flash('File(s) successfully uploaded')
		else:
			flash('ERROR: Allowed filetypes are mp3, flac, wav')
			return redirect(request.url)
	return "Hello World"