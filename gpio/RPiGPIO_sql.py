#!/usr/bin/python3
import time
import datetime
import RPi.GPIO
import sqlite3

# Initialise RPi.GPIO
uit = RPi.GPIO.HIGH
aan = RPi.GPIO.LOW
outputList = (29, 31, 33, 35)
RPi.GPIO.setmode(RPi.GPIO.BOARD)
RPi.GPIO.setup(outputList, RPi.GPIO.OUT, initial=uit)

# Initialise sqlite
con = sqlite3.connect('../testdata.db')
cur = con.cursor()

# Initialise data
nu = datetime.datetime.now()
print(nu.hour)
print(nu.minute)
export_startuur = 0
export_startmin = 0

# Get user input
export_startuur = input("Please enter start hour:\n")
print(f'You entered {export_startuur} uur')
export_startmin = input("Please enter start minute:\n")
print(f'You entered {export_startmin} minuten')

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS testtable
            (data_1 INT, data_2 INT)''')

# Export
# Update a row of data
cur.execute("UPDATE testtable SET data_1 = ?, data_2 = ?", (export_startuur,
                                                            export_startmin))
print("Data verzonden")

# Save (commit) the changes
con.commit()

# Import
# Select data from table
cur.execute("SELECT * FROM testtable")
data = cur.fetchone()
print(data)
import_startuur = data[0]
import_starmin = data[1]
print(import_startuur)
print(import_starmin)

# Process
if import_startuur == nu.hour and import_starmin > nu.minute:
    RPi.GPIO.output(29, aan)
    print("1 AAN")
else:
    RPi.GPIO.output(29, uit)
    print("1 UIT")

# Close sql connection
con.close()

# Cleanup
RPi.GPIO.cleanup()
print("CLEANUP")
