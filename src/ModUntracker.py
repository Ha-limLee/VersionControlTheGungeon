import sqlite3
from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout
from .ModTable import ModTable

class ModUntracker:
    def __init__(self):
        self.table: ModTable = None
        pass

    def addTable(self, table):
        self.table = table
    
    def untrack(self):
        selectedIds = self.table.getSelectedIds()


        parameters = [(id,) for id in selectedIds]

        conn = sqlite3.connect('versionTBL')
        cur = conn.cursor()
        
        cur.executemany('DELETE FROM versionTBL WHERE id=?;', parameters)

        conn.commit()
        conn.close()

        self.table.refresh()
        pass

class ModUntrackerBtn(QWidget):
    def __init__(self):
        super().__init__()
        self.modUntracker: ModUntracker = None
        self.btn = QPushButton('Untrack selected')

        layout = QGridLayout()
        layout.addWidget(self.btn)

        self.setLayout(layout)

        self.btn.clicked.connect(self.untrack)

        pass

    def addUntracker(self, untracker):
        self.modUntracker = untracker

    def untrack(self):
        self.modUntracker.untrack()