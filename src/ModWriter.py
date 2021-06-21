import sqlite3

class ModWriter:
    def __init__(self):
        self.observers = []
        self.conn = sqlite3.connect('versionTBL')
        self.cur = self.conn.cursor()
        try:
            self.cur.execute('''
                CREATE TABLE versionTBL (
                    id TEXT PRIMARY KEY NOT NULL,
                    name TEXT NOT NULL,
                    version TEXT,
                    date TEXT NOT NULL,
                    path TEXT NOT NULL
                );
            ''')
        except:
            pass

        self.conn.close()
        pass

    def addObserver(self, observer):
        if not observer in self.observers:
            self.observers.append(observer)

    def update(self, data):
        print('in observer')
        self.conn = sqlite3.connect('versionTBL')
        self.cur = self.conn.curosr()

        argument = [tuple(each.values()) for each in data]
        
        self.cur.executemany(
            'INSERT INTO versionTBL VALUES (?, ?, ?, ?, ?)',
            argument
        )
        
        self.conn.commit()
        self.conn.close()
        
        for each in self.observers:
            each.refresh()