import sqlite3
import time
import zlib
import string
import nltk
from nltk.corpus import stopwords
stopwords.words('english')
en_stops = set(stopwords.words('english'))

conn = sqlite3.connect('omdb.sqlite')
cur = conn.cursor()

fh = cur.execute('SELECT plotlong FROM Omdbdata')

counts = dict()
for row in fh :
    text = row[0]
    text = text.translate(str.maketrans('','',string.punctuation))
    text = text.translate(str.maketrans('','','1234567890'))
    text = text.strip()
    text = text.lower()
    words = text.split()
    for word in words:
        if len(word) < 4 : continue
        if word not in en_stops: #filter nltk stopwords
            counts[word] = counts.get(word,0) + 1

x = sorted(counts, key=counts.get, reverse=True)
highest = None
lowest = None
for k in x[:100]:
    if highest is None or highest < counts[k] :
        highest = counts[k]
    if lowest is None or lowest > counts[k] :
        lowest = counts[k]
print('Range of counts:',highest,lowest)

# Spread the font sizes across 20-100 based on the count
bigsize = 80
smallsize = 20

fhand = open('omword.js','w')
fhand.write("omword = [")
first = True
for k in x[:100]:
    if not first : fhand.write( ",\n")
    first = False
    size = counts[k]
    size = (size - lowest) / float(highest - lowest)
    size = int((size * bigsize) + smallsize)
    fhand.write("{text: '"+k+"', size: "+str(size)+"}")
fhand.write( "\n];\n")
fhand.close()

print("Output written to omword.js")
print("Open omword.htm in a browser to see the vizualisation")
