import sqlite3
import string
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

conn = sqlite3.connect('omdb.sqlite')
cur = conn.cursor()

fh = cur.execute('SELECT runtime, year FROM Omdbdata;')
counts = dict()
rts = list()
years = list()
for line in fh:
    rt = line[0]
    rt = rt.replace(' min', '')
    rt = int(rt)
    rts.append(rt)
    if rt not in counts:
        counts[rt] = 1
    else:
        counts[rt] += 1
    year = line[1]
    year = int(year)
    years.append(year)

# Am keeping years info for some more advanced processing
#print(rts[:30])
print('Runtimes: ', len(rts))
print('Years: ', len(years))
print('Close graph window to exit program.')
#print(years[:30])

# generate histogram
lst = list()
for key, val in list(counts.items()):
    lst.append((val, key))

newlst = lst

countdata = list()
rtdata = list()
for item in newlst:
    countdata.append(item[0])
    rtdata.append(item[1])
#print(rtdata)
#print(countdata)

# make pandas dataframe
data = {'Count':countdata, 'Runtime':rtdata}
df = pd.DataFrame(data)

# output seaborn density plot // next up prettify graph and fine tune axis
sns.set(style='darkgrid')
sns.kdeplot(df['Runtime'])
plt.show()



 