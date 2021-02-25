#!/usr/bin/python3
import sqlite3

# Initialise sqlite
con = sqlite3.connect('testdata.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS testtable
            (data_1 REAL, data_2 REAL)''')

# Select data from table
# cur.execute("SELECT data_1 FROM testtable")
# data = cur.fetchone()[0]
cur.execute("SELECT * FROM testtable")
data = cur.fetchone()
print(data)
data_1 = data[0]
data_2 = data[1]
print(data_1)
print(data_2)

# Select all data ordered
# for row in cur.execute("SELECT * FROM testtable ORDER BY data_1"):
#     print(row)

# Initialise data lists
# data_1 = []
# data_2 = []
# Select all data and append list
# cur.execute("SELECT * FROM testtable")
# data = cur.fetchall()
# for row in data:
#     data_1.append(row[0])
#     data_2.append(row[1])

print("Data gelezen")

# Close connection
con.close()
