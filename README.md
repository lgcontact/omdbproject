# omdbproject
Capstone project for Python for Everybody course, practising web access, databases and data visualisation with Python.

1. run omload.py (which includes a routine that loads CSV data into a table then reads each line of the table and queries omdbapi.com and retrieves film data)

2. run omclean.py (which cleans up the raw data and puts it into new tables; there is more to be done here when I have a better grasp of relational databases but for now it works)

3. Visualisation 1: omword.py (which creates a histogram from the plot summaries, filters unimportant words out with nltk stopwords and outputs a wordcloud)

4. Visualisation 2: omcounter.py (which counts and sorts the appearances of actors in the 1000 films and outputs a Bokeh bar graph with some customisation)

5. Visualisation 3: omrt.py (which creates a seaborn density plot after making a pandas dataframe)

It was fun getting to know all these tools; of course there is lots more functionality and prettification of the visualisations I could do, and many programming things I could do better. I look forward to becoming more confident in building relational tables to model the data better, but this is all for now.
