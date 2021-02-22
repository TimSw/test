import sqlite3


# Initiate SQLite
con = sqlite3.connect("data.db")
cur = con.cursor()

# Create table
cur.execute("""CREATE TABLE IF NOT EXISTS temperatuur
    (datetime text, temperatuur real)""")

# Select data
#cur.execute('SELECT datetime, temperatuur FROM temperatuur LIMIT 5')
#cur.execute('SELECT * FROM temperatuur LIMIT 5')
#cur.execute('SELECT * FROM temperatuur')
#cur.execute('SELECT * FROM temperatuur ORDER BY datetime')
cur.execute("SELECT * FROM temperatuur LIMIT 5 OFFSET (SELECT COUNT(*) "
            "FROM temperatuur)-5")
data = cur.fetchall()
#data = cur.fetchmany(5)

print(data)

# Save (commit) the changes
con.commit()

# Close connection
con.close()
