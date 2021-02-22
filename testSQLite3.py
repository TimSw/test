import time
import random
import sqlite3


con = sqlite3.connect('data.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS temperature
    (timestamp real, temperature real)''')


def insert_data():
    now = time.time()
    temp = random.randint(-5.00, 25.00)

    print(now)

    # Insert a row of data
    cur.execute("INSERT INTO temperature VALUES (?, ?)", (now, temp))

    # Save (commit) the changes
    con.commit()
    print("Data added")


for i in range(100):
    print(i)
    insert_data()
    time.sleep(2)


# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()
print("Close")
