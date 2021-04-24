import sqlite3

def make_test_db():
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    con.execute('CREATE TABLE mods(\
        id TEXT, name TEXT, version TEXT)')
    
    cur.executemany('INSERT INTO mods VALUES (?, ?, ?)',
        [
            ('100000', 'mod1', '1.0.0'),
            ('100002', 'mod2', '1.0.1'),
            ('100003', 'mod3', '2.0.1')
        ]
    )

    cur.close()
    con.commit()
    con.close()

def show_test_db():
    con = sqlite3.connect("test.db")
    cur = con.cursor()
    rows = cur.execute('SELECT name, version FROM mods')
    for row in rows:
        print(row)

if __name__ == "__main__":
    show_test_db()
    