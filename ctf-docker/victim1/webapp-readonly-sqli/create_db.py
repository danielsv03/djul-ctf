# create_db.py
import sqlite3
db = sqlite3.connect('ctf_readonly.db')
cur = db.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY, name TEXT, description TEXT);')
cur.execute('DELETE FROM products;')
# normal entries
cur.execute("INSERT INTO products(name,description) VALUES(?,?)", ("widget", "A regular widget"))
cur.execute("INSERT INTO products(name,description) VALUES(?,?)", ("gadget", "A boring gadget"))
# secret entry - contains victim2 password (the thing players must find)
cur.execute("INSERT INTO products(name,description) VALUES(?,?)",
            ("super-secret-ssh-password-woah", "movement"))
db.commit()
db.close()
print("DB created: ctf_readonly.db")