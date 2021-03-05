#!/usr/bin/python3
import sqlite3

# Initialise sqlite
con = sqlite3.connect('../testdata.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS testtable 
            (data_column_1 TEXT, data_column_2 INTEGER, data_column_3 INTEGER)''')

# Select data from table
kolomnaam = ("testtimer_3", )
cur.execute('''SELECT * FROM testtable WHERE data_column_1 = ?''', kolomnaam)
data = cur.fetchone()
print(data)
timer = data[0]
hour = data[1]
minute = data[2]

print(timer)
print(hour)
print(minute)

print("Data gelezen")

# Close connection
con.close()
