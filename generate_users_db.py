import sqlite3

conn = sqlite3.connect('user_credentials.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             first_name TEXT NOT NULL,
             last_name TEXT NOT NULL,
             email TEXT NOT NULL,
             username TEXT NOT NULL,
             password TEXT NOT NULL)''')

conn.commit()
conn.close()