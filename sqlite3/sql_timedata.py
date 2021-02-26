#!/usr/bin/python3
import sqlite3

# Initialise data
hour = 1
minute = 00
timer = "testtimer"

# Initialise sqlite
con = sqlite3.connect('../testdata.db')
cur = con.cursor()

# Fill data
data = (hour, minute, timer)

# Print data
print(data)

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS time
                    (timer TEXT, hour INTEGER, minute INTEGER)''')

# Update data
cur.execute("UPDATE time SET hour = ?, minute = ? WHERE timer = ?",
            data)

# Save (commit) the changes
con.commit()

# Close connection
con.close()

# Print
print("Update ended")
