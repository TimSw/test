#!/usr/bin/python3
import datetime
import random
import sqlite3

# Define variables
nu = datetime.datetime.now()
nummer = random.random()

print(nu, nummer)

# Initialise sqlite
con = sqlite3.connect('../testdata.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS testtable
            (data_1 REAL, data_2 REAL)''')

# Insert a row of data
# cur.execute("INSERT INTO testtable VALUES (?, ?)", (nu, nummer))

# Update a row of data
cur.execute("UPDATE testtable SET data_1 = ?, data_2 = ?", (nu, nummer))

print("Data verzonden")

# Save (commit) the changes
con.commit()

# Close connection
con.close()
