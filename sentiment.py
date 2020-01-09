import nltk 
import matplotlib.pyplot as plt
from transcribe import transcribe_audio

from nltk.tokenize import sent_tokenize
text = transcribe_audio('transcript.mp3')
tokenized_text=sent_tokenize(text)
#print("Tokenized text: ", tokenized_text)
#print('\n')

from nltk.tokenize import word_tokenize
tokenized_word=word_tokenize(text)
#print('Tokenized word: ', tokenized_word)


from nltk.corpus import stopwords
stop_words=set(stopwords.words("english"))
#print('Stop words: ', stop_words)


#Removing Stopwords to make Filtered Sentence
filtered_sent=[]
for w in tokenized_word:
    if w not in stop_words:
        filtered_sent.append(w)
#print("Tokenized Sentence:",tokenized_word)
#print("Filterd Sentence:",filtered_sent)

#Filtered Sentence: ['conscious', 'spiritual', 'moral', 'Heritage', 'union', 'founded', 
#'indivisible', 'Universal', 'values', 'human', 'dignity', 'Freedom', 'equality', 'solidarity', 'based', 'principles', 'democracy', 
#'rule', 'law', 'places', 'individual', 'heart', 'activities', 'establishing', 'citizenship', 'union', 'creating', 'area', 'Freedom', 
#'security', 'justice']


# Stemming
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
ps = PorterStemmer()

stemmed_words=[]
for w in filtered_sent:
    stemmed_words.append(ps.stem(w))

#pyprint("Filtered Sentence:",filtered_sent)
#print("Stemmed Sentence:",stemmed_words)
#Stemmed Sentence: ['consciou', 'spiritu', 'moral', 'heritag', 'union', 'found', 'indivis', 'univers', 'valu', 'human', 'digniti', 
# 'freedom', 'equal', 'solidar', 'base', 'principl', 'democraci', 'rule', 'law', 'place', 'individu', 'heart', 'activ', 'establish', 
# 'citizenship', 'union', 'creat', 'area', 'freedom', 'secur', 'justic']


#Lexicon Normalization
#performing stemming and Lemmatization

from nltk.stem.wordnet import WordNetLemmatizer
lem = WordNetLemmatizer()

from nltk.stem.porter import PorterStemmer
stem = PorterStemmer()

#word = "flying"

lemmatized_word=[]
for w in filtered_sent: 
    lemmatized_word.append(lem.lemmatize(w, "v"))

##print("Lemmatized Word:", lemmatized_word)


#print("Lemmatized Word:",lem.lemmatize(word,"v"))
#print("Stemmed Word:",stem.stem(word))

#Part-of-Speech(POS) tagging
tokens=nltk.word_tokenize(text)
#print(tokens)
print(nltk.pos_tag(tokens))