import sqlite3
import string
import bokeh
from bokeh.plotting import figure, output_file, show

qty = input('How many actors do you want to list?')
if (len(qty) < 1): qty = 25
qty = int(qty)


conn = sqlite3.connect('omdb.sqlite')
cur = conn.cursor()

fh = cur.execute('SELECT name FROM Actors;')
counts = dict()
for line in fh:
    line = str(line)
    line = line.translate(str.maketrans('', '', string.punctuation))
    if line not in counts:
        counts[line] = 1
    else:
        counts[line] += 1

# Sort the dictionary by value
lst = list()
for key, val in list(counts.items()):
    lst.append((val, key))

lst.sort(reverse=True)

for key, val in lst[:30]:
    print(key, val)

#print(lst)
newlst = lst[:qty]
#newlst.sort(reverse=True)
#print(newlst)
newkeys = list()
newvals = list()
for item in newlst:
    newvals.append(item[0])
    newkeys.append(item[1])
print(newvals)
print(newkeys)

counts = newvals
names = newkeys
    
#create Bokeh bar chart
  
# file to save the model
output_file("omcount.html")
      
# instantiating the figure object
graph = figure(y_range=names, height=600, width=600, toolbar_location=None, tools="", title="Frequency of Actors in Top 1000 Films")
# with some formatting options
graph.title.align = "right"
graph.title.text_color = "orange"
graph.title.text_font_size = "25px" 

graph.hbar(y=names, right=counts, height=0.5, width=0.9)

#graph.xgrid.grid_line_color = None
#graph.y_range.start = 0

show(graph)
