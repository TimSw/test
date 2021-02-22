import sqlite3
import matplotlib
import matplotlib.pyplot as plt
from dateutil import parser


# Only needed when using matplotlib on pythonanywhere
matplotlib.use("Agg")

con = sqlite3.connect('data.db')
cur = con.cursor()

x1data = []
y1data = []
x2data = []
y2data = []

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS temperatuur
    (datetime text, temperatuur real)''')

# Select all data ordered and append lists
cur.execute("SELECT * FROM temperatuur ORDER BY datetime")
data = cur.fetchall()
for row in data:
    x1data.append(parser.parse(row[0]))
    y1data.append(row[1])

# Average value
average = sum(y1data) / float(len(y1data))
for i in y1data:
    y2data.append(average)
x2data = x1data

print(average, "\n")
print(x1data, "\n")
print(y1data, "\n")
print(x2data, "\n")
print(x2data, "\n")

# Plot graph
fig = plt.figure()

plt.title("Testlabel", fontdict=None, loc='center', pad=None)
plt.plot(x1data, y1data, label="Actuele")
plt.plot(x2data, y2data, label="Gemiddelde")
plt.ylabel("Temperatuur")
plt.xlabel("Timestamp")
plt.title("Temperatuurgrafiek\nBinnentemperatuur")
plt.legend()
plt.grid(True)

# beautify the x-labels
plt.gcf().autofmt_xdate()

plt.show()

fig.savefig("graph.png")

print("einde")
