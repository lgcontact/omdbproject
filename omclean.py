import sqlite3

conn = sqlite3.connect('omdb.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Actors;
DROP TABLE IF EXISTS Directors;
DROP TABLE IF EXISTS Genres;
DROP TABLE IF EXISTS IDs;
DROP TABLE IF EXISTS Main;

CREATE TABLE Main (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT,
    actor TEXT, director TEXT, genre TEXT, runtime TEXT
);

CREATE TABLE IDs (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title    TEXT UNIQUE,
    actor_id INTEGER, director_id INTEGER, genre_id INTEGER, runtime INTEGER
);

CREATE TABLE Actors (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT
);

CREATE TABLE Directors (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE,
    director_id INTEGER
);

CREATE TABLE Genres (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    genre   TEXT UNIQUE,
    genre_id INTEGER
);
''')

actors = list()
afh = cur.execute('SELECT actors FROM Omdbdata;')
for aline in afh: #ideal to simplify and make a function of repeated instructions but it works for now
    aitems = list(aline)
    for aitem in aitems:
        asepitems = aitem.split(",")
        for asepitem in asepitems:
            actors.append(asepitem.strip())
for actor in actors:
    conn.execute('''INSERT OR IGNORE INTO Actors (name) 
    VALUES ( ? )''', ( actor, ) )
    conn.execute('''INSERT OR IGNORE INTO Main (actor) 
    VALUES ( ? )''', ( actor, ) )
conn.commit()
            
directors = list()
dfh = cur.execute('SELECT director FROM Omdbdata;')
for dline in dfh:
    ditems = list(dline)
    for ditem in ditems:
        dsepitems = ditem.split(",")
        for dsepitem in dsepitems:
            directors.append(dsepitem.strip())
for director in directors:
    conn.execute('''INSERT OR IGNORE INTO Directors (name) 
    VALUES ( ? )''', ( director, ) )
conn.commit()            

genres = list()
gfh = cur.execute('SELECT genre FROM Omdbdata;')
for gline in gfh:
    gitems = list(gline)
    for gitem in gitems:
        gsepitems = gitem.split(",")
        for gsepitem in gsepitems:
            genres.append(gsepitem.strip())
for genre in genres:
    conn.execute('''INSERT OR IGNORE INTO Genres (genre) 
    VALUES ( ? )''', ( genre, ) )
conn.commit()        

#hmm,this is stripping the text and turning it into an integer fine but not keeping it associated with the title; need to do the strip in the main table
# runtimes = list()
# rfh = cur.execute('SELECT runtime FROM Omdbdata;')
# for rline in rfh:
    # rtitems = list(rline)
    # for rtitem in rtitems:
        # rt = rtitem.replace(" min","")
        # rti = int(rt)
        # runtimes.append(rti)
#print(runtimes)
            
print(actors[:20])
print(directors[:20])
print(genres[:20])





