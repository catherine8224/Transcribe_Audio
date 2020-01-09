import numpy as np
#import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
from os import path
import matplotlib.pyplot as plt

import speech_recognition as sr
from os import path
from pydub import AudioSegment
import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf 


def wordcloud_something(flee):
    sound = AudioSegment.from_mp3(flee)
    sound.export("transcript.wav", format="wav")

    AUDIO_FILE = "transcript.wav"

    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)
    transcription = r.recognize_google(audio) #class 'str'
    text = (transcription)

    american_flag = np.array(Image.open("american_flag.png"))

    wordcloud = WordCloud( width = 480, height = 480, 
    background_color ='white', 
    max_words = 20,
    mask = american_flag,
    #stopwords = stopwords, 
    min_font_size = 10
    ).generate(text) 
# plot the WordCloud image                        
#plt.figure(figsize = (8, 8), facecolor = None) 
# plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear') 
    plt.axis("off") 
    plt.margins(x=0, y=0)
    plt.savefig("img/ita_wine.png", format="png")
    #img = BytesIO()
    #wordcloud.to_image().save(img, 'PNG')
    #img.seek(0)
    #return send_file(img, mimetype='image/png')

    #return(plt.show())
    #plt.tight_layout(pad = 0) 
    #wordcloud.to_file("wordCloud.png") 

#wordcloud_something('transcript.mp3')

# @app.route('/wordcloud/<vendor_duns>')
# def images(vendor_duns):
#     words = Words.query.filter(Words.vendor_duns == vendor_duns).with_entities(Words.words).all()
#     # t = [r.__dict__ for r in words]
#     # print(t)
#     one_row = list(itertools.chain.from_iterable(words))
#     text = ' '.join(one_row)
#     return render_template("upload.html", text=text)

