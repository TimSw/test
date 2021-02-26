import datetime
import sqlite3


con = sqlite3.connect('data.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS testdatetime
    (datetime text)''')

# Create timestamp
nu = datetime.datetime.now()
print(nu)

# Insert a row of data
cur.execute("INSERT INTO testdatetime VALUES (?)", (nu,))
print("Data toegevoegd")

# Select all data ordered
for row in cur.execute("SELECT * FROM testdatetime ORDER BY datetime"):
    print(row)
print("Data gelezen")

# Save (commit) the changes
con.commit()

