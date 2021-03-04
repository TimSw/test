#!/usr/bin/python3
import datetime
import sqlite3

# Define variables
# Initialise current time
nu = datetime.datetime.now()
uur = nu.hour
minuut = nu.minute
kolomnaam = "testtimer_3"

print("Het is", uur, "uur")
print("en", minuut, "minuten")

# Initialise sqlite
con = sqlite3.connect('../testdata.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS testtable 
            (data_column_1 TEXT, data_column_2 INTEGER, data_column_3 INTEGER)''')

# Insert a row of data
data = (kolomnaam, uur, minuut)
cur.execute('''INSERT INTO testtable (data_column_1, data_column_2, data_column_3)
            VALUES (?, ?, ?)''', data)

# Update a row of data
# data = (uur, minuut, kolomnaam)
# cur.execute('''UPDATE testtable SET data_column_2 = ?, data_column_3 = ?
#             WHERE data_column_1 = ?''', data)

print("Data verzonden")

# Save (commit) the changes
con.commit()

# Close connection
con.close()
