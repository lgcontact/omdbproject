import urllib.request, urllib.parse, urllib.error
import sqlite3
import json
import ssl
import csv

#load csv file into table
csvfile = input('Enter CSV file to load: ')
if (len(csvfile) < 1): csvfile = 'top1000.csv'

conn = sqlite3.connect('omdb.sqlite')
cur = conn.cursor()

csv_data = csv.reader(open(csvfile))
header = next(csv_data)

cur.execute('DROP TABLE IF EXISTS Top1000')

#Rank	Title	Genre	Description	Director	Actors	Year	Runtime (Minutes)	Rating	Votes	Revenue (Millions)	Metascore

cur.execute('''CREATE TABLE top1000
    (id INTEGER PRIMARY KEY UNIQUE, rank INTEGER, title TEXT, genre TEXT, description TEXT,
    director TEXT, actors TEXT, year INTEGER, runtime INTEGER,
    rating REAL)''')

print('Importing CSV rows')
for row in csv_data:
    print(row)
    rank = row[0]
    title = row[1]
    genre = row[2]
    description = row[3]
    director = row[4]
    actors = row[5]
    year = row[6]
    runtime = row[7]
    rating = row[8]
    
    cur.execute('''
        INSERT INTO Top1000 (rank, title, genre, description, director, actors, year, runtime, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (rank, title, genre, description, director, actors, year, runtime, rating))
        
conn.commit()
cur.close()
print('Done')

#then process each line of the CSV file

#this API key won't work for long, but you can get a free or cheap subscription at omdbapi.com
api_key = "800a5c3b"
serviceurl = "http://www.omdbapi.com/?"

conn = sqlite3.connect('omdb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Omdbdata;')
cur.execute('''CREATE TABLE Omdbdata (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
title TEXT, year TEXT, rated TEXT, released TEXT, runtime TEXT, genre TEXT, director TEXT, 
writer TEXT, actors TEXT, plotlong TEXT, language  TEXT, country TEXT, awards TEXT, poster URL, 
imdbrating REAL, rtrating REAL, mcrating REAL, imdbid TEXT, type TEXT, dvd TEXT, boxoffice TEXT, 
production TEXT, website URL)
''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

fh = cur.execute('''SELECT id, title, year FROM top1000''')

rty = list()
for row in fh:
    #row = cur.fetchone()
    qtitle = str(row[1])
    qyear = str(row[2])

    #print(rty)
    print(qtitle)
    print(qyear)

    #parms sets up the query url: url concatenated with address and api key
    #query format https://www.omdbapi.com/?t=blade+runner&y=2018&plot=full&apikey=800a5c3b

    parms = dict()
    parms["t"] = qtitle
    parms["y"] = qyear
    parms["plot"] = "full"
    parms["apikey"] = api_key
    url = serviceurl + urllib.parse.urlencode(parms)

    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))
    
    js = json.loads(data)
    if js['Response'] == 'False':
        print('==== Failure To Retrieve ====')
        print(data)
        continue
   
    title = js['Title']
    year = js['Year']
    rated = js['Rated']
    released = js['Released']
    runtime = js['Runtime']
    genre = js['Genre']
    director = js['Director']
    writer = js['Writer']
    actors = js['Actors']
    plotlong = js['Plot']
    language = js['Language']
    country = js['Country']
    awards = js['Awards']
    poster = js['Poster']
    imdbrating = js['imdbRating']
    mcrating = js['Metascore']
    imdbid = js['imdbID']
    qtype = js['Type']
    dvd = js['DVD']
    boxoffice = js['BoxOffice']
    production = js['Production']
    website = js['Website']
    try:
        rtrating = js['Ratings'][1]['Value']
    except:
        rtrating = 'N/A'
    
    print(title)
    print(imdbid)
    print(runtime)
    
    conn.execute('''INSERT INTO Omdbdata (title, year, rated, released, runtime, genre, director, 
    writer, actors, plotlong, language, country, awards, poster, imdbrating, rtrating, mcrating, 
    imdbid, type, dvd, boxoffice, production, website) 
    VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''', (title, year, rated, released, runtime, genre, director, writer, actors, plotlong, language, country, awards, poster, imdbrating, rtrating, mcrating, imdbid, qtype, dvd, boxoffice, production, website) )

    conn.commit()

print("Done")
