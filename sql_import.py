#!/usr/bin/python3
import sqlite3

# Define variables


# Initialise sqlite
con = sqlite3.connect('testdata.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS testtable
            (data_1 REAL, data_2 REAL)''')

# Select all data ordered
for row in cur.execute("SELECT * FROM testtable ORDER BY data_1"):
    print(row)
print("Data gelezen")

# Close connection
con.close()
