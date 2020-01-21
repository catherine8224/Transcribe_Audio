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



#analyzes the whole text 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

def vader(document):
    message_text = document
    # Calling the polarity_scores method on sid and passing in the message_text outputs a dictionary with negative, neutral, positive, and compound scores for the input text
    scores = sid.polarity_scores(message_text)
# Here we loop through the keys contained in scores (pos, neu, neg, and compound scores) and print the key-value pairs on the screen
    for key in sorted(scores):
            open_string = '{0}: {1}, '.format(key, scores[key])
            return open_string, scores



# below is the sentiment analysis code rewritten for sentence-level analysis
# note the new module -- word_tokenize!
import nltk.data
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import sentiment
from nltk import word_tokenize

def each_word(document):
    # Next, we initialize VADER so we can use it within our Python script
    sid = SentimentIntensityAnalyzer()

    # We will also initialize our 'english.pickle' function and give it a short name

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    message_text =  document
    # The tokenize method breaks up the paragraph into a list of strings. In this example, note that the tokenizer is confused by the absence of spaces after periods and actually fails to break up sentences in two instances. How might you fix that?

    sentences = tokenizer.tokenize(message_text)

    # We add the additional step of iterating through the list of sentences and calculating and printing polarity scores for each one.

    for sentence in sentences:
            print(sentence)
            scores = sid.polarity_scores(sentence)
            for key in sorted(scores):
                    print('{0}: {1}, '.format(key, scores[key]), end='')
            print()