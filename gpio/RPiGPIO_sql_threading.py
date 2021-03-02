#!/usr/bin/python3
import time
import datetime
import RPi.GPIO
import sqlite3
import threading

# Initialise RPi.GPIO
uit = RPi.GPIO.HIGH
aan = RPi.GPIO.LOW
outputList = (29, 31, 33, 35)
RPi.GPIO.setmode(RPi.GPIO.BOARD)
RPi.GPIO.setup(outputList, RPi.GPIO.OUT, initial=uit)

# Initialise data


def get_input():
    while True:
        try:
            # Initialise sqlite
            con = sqlite3.connect('../testdata.db')
            cur = con.cursor()

            # Initialise current time
            nu = datetime.datetime.now()
            print("Het is", nu.hour, "uur")
            print("en", nu.minute, "minuten")
            export_startuur = input("Please enter start hour:\n")
            print(f'You entered {export_startuur} hour')
            export_startmin = input("Please enter start minute:\n")
            print(f'You entered {export_startmin} minutes')

            # Create table
            cur.execute('''CREATE TABLE IF NOT EXISTS testtable
                        (data_1 INT, data_2 INT)''')

            # Update a row of data
            cur.execute("UPDATE testtable SET data_1 = ?, data_2 = ?",
                        (export_startuur, export_startmin))
            print("Data verzonden")

            # Save (commit) the changes
            con.commit()

        except Exception as e:
            print(e)
            # Close sql connection
            con.close()


def process_imput():
    while True:
        try:
            # Initialise sqlite
            con = sqlite3.connect('../testdata.db')
            cur = con.cursor()

            # Initialise current time
            nu = datetime.datetime.now()
            print("Het is", nu.hour, "uur")
            print("en", nu.minute, "minuten")
            # Select data from table
            cur.execute("SELECT * FROM testtable")
            data = cur.fetchone()
            print(data)
            import_startuur = data[0]
            import_starmin = data[1]
            print(import_startuur)
            print(import_starmin)

            if import_startuur == nu.hour and import_starmin > nu.minute:
                RPi.GPIO.output(29, aan)
                print("1 AAN")
                print("Sleep for 10 seconds")
                time.sleep(10)

            else:
                RPi.GPIO.output(29, uit)
                print("1 UIT")
                print("Sleep for 10 seconds")
                time.sleep(10)

        except Exception as e:
            print(e)
            # Close sql connection
            con.close()


if __name__ == "__main__":
    # Threading
    print("Voor creëren thread 1")
    t1 = threading.Thread(target=get_input)
    print("Voor creëren thread 2")
    t2 = threading.Thread(target=process_imput)
    print("Voor starten thread 1")
    t1.start()
    print("Voor starten thread 2")
    t2.start()

    # Cleanup
    RPi.GPIO.cleanup()
    print("CLEANUP")
