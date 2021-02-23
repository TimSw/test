import datetime
import random
import sqlite3

nu = datetime.datetime.now()
temp = random.random()

con = sqlite3.connect('data.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS temperatuur
    (datetime text, temperatuur real)''')

# Select all data ordered
for row in cur.execute("SELECT * FROM temperatuur ORDER BY datetime"):
    print(row)

print("Data gelezen")

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()
print("sluit")