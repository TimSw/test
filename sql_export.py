#!/usr/bin/python3
import datetime
import random
import sqlite3

# Define variables
nu = datetime.datetime.now()
number = random.random()
print(nu, number)

# Initialise sqlite
con = sqlite3.connect('testdata.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS testtable
            (data_1 REAL, data_2 REAL)''')

# Insert a row of data
cur.execute("INSERT INTO testtable VALUES (?, ?)", (nu, number))
print("Data verzonden")

# Save (commit) the changes
con.commit()

# Close connection
con.close()
