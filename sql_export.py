import datetime
import random
import sqlite3

# Define variables
nu = datetime.datetime.now()
temp = random.random()
print(nu, temp)

# Initialise sqlite
con = sqlite3.connect('testdata.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS testtable
    (data_1 REAL, data_2 real)''')

# Insert a row of data
cur.execute("INSERT INTO testtable VALUES (?, ?)", (nu, temp))
print("Data verzonden")

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()

