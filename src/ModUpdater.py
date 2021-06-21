from PySide6.QtWidgets import QGridLayout, QWidget, QPushButton
import sqlite3
import os
from functools import reduce

from .ModTable import ModTable

class ModUpdater:
    def __init__(self):
        self.updatables: list = None
        self.table: ModTable = None

    def addUpdatables(self, updatables):
        self.updatables = updatables
    
    def addTable(self, table):
        self.table = table

    def writeMod(self):
        conn = sqlite3.connect('versionTBL')
        cur = conn.cursor()

        if len(self.updatables) > 0:
            path = cur.execute('SELECT path FROM versionTBL').fetchone()[0]
            temp = path.split('/')[0:-1]
            modtxt = reduce(lambda x,y: x+'/'+y, temp) + '/mods.txt'
            if os.path.isfile(modtxt):
                os.remove(modtxt)

        for each in self.updatables:
            id = each.getId()
            date = each.getDate()
            fileName: str = each.getName()
            
            prevPath = cur.execute(f'SELECT path FROM versionTBL WHERE id={id}').fetchone()[0]
            temp = prevPath.split('/')[0:-1]
            newPath = reduce(lambda x,y: x+'/'+y, temp) + '/' + fileName

            os.remove(prevPath)
            newFile = open(newPath, 'wb')
            content = each.getContent()
            newFile.write(content)
            newFile.close()

            cur.execute('UPDATE versionTBL SET date=? WHERE id=?', (date, id))

            modName, modVersion = fileName.replace('.zip', '').split('_')[1:3]
            self.table.notifyUpdateFinished(id, modName, modVersion)

        conn.commit()
        conn.close()

class ModUpdaterBtn(QWidget):
    def __init__(self):
        super().__init__()
        self.modUpdater: ModUpdater = None
        self.btn = QPushButton('Update')

        layout = QGridLayout()
        layout.addWidget(self.btn)

        self.setLayout(layout)

        self.btn.clicked.connect(self.execute)

    def addModUpdater(self, modUpdater):
        self.modUpdater = modUpdater
    
    def execute(self):
        self.modUpdater.writeMod()