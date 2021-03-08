#!/usr/bin/python3
import threading
import time
import RPi.GPIO
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

print("timer = ", timer)
print("hour = ", hour)
print("minute = ", minute)

print("Data gelezen")

# Close connection
con.close()


class Light:
    def __init__(self):
        self.light_1 = 1
        self.light_2 = 0

    testvariabele_1 = 1

    def light(self):
        while True:
            if self.light_1 == 1:
                self.light_2 = 1
                print("self.light_2 = ", self.light_2)
                RPi.GPIO.output(29, False)
                print("OUTPUT LIGHT ON")
                time.sleep(10)
            else:
                self.light_2 = 2
                print("self.light_2 = ", self.light_2)
                RPi.GPIO.output(29, True)
                print("OUTPUT LIGHT ON")
                time.sleep(10)

    def run(self):
        t1 = threading.Thread(target=self.light)
        # t1 = threading.Thread(target=self.light, daemon=True)
        t1.start()


if __name__ == "__main__":
    print(Light.testvariabele_1)
    l1 = Light()
    l1.run()
