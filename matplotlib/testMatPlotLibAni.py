import sqlite3
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dateutil import parser


# Initiate DB
con = sqlite3.connect('data.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS temperatuur
    (datetime text, temperatuur real)''')

# Initiate MatPlotLib
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)


def animate(i):

    # Select all data ordered and append lists
    cur.execute("SELECT * FROM temperatuur ORDER BY datetime")
    data = cur.fetchall()

    x1data = []
    y1data = []
    x2data = []
    y2data = []

    for row in data:
        x1data.append(parser.parse(row[0]))
        y1data.append(row[1])

    # Average value
    average = sum(y1data) / float(len(y1data))
    for items in y1data:
        y2data.append(average)
    x2data = x1data

    print(x1data, "\n")
    print(y1data, "\n")
    print(x2data, "\n")
    print(y2data, "\n")

    ax1.clear()
    ax1.plot(x1data, y1data)


ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.title("Testlabel", fontdict=None, loc='center', pad=None)
plt.ylabel("Temperatuur")
plt.xlabel("Timestamp")
plt.title("Temperatuurgrafiek\nBinnentemperatuur")
plt.legend()
plt.grid(True)

fig.savefig("graph.png")
plt.show()

print("einde")
