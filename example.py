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
print(list(data))
print(list(data.values()))

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

print(make_bargraph(data))
