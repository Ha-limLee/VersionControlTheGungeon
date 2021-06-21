from PySide6.QtWidgets import QGridLayout, QPushButton, QTableWidget, QAbstractItemView, QTableWidgetItem, QWidget
from PySide6.QtCore import Qt
import os
import sqlite3
import asyncio

class ModTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.headerLabels = ['ID', 'Mod name', 'Current version', 'Status']

        self.updatables: list = None

        self.setColumnCount(len(self.headerLabels))

        self.setHorizontalHeaderLabels(self.headerLabels)

        if os.path.isfile('versionTBL'):
            self.refresh()
            pass
        
        pass

    def getSelectedIds(self) -> list:
        selectedRows = set(index.row() for index in self.selectedIndexes())
        idColumn = self.headerLabels.index('ID')
        
        res = [self.item(row, idColumn).text() for row in selectedRows]
        return res

    def addUpdatables(self, updatables):
        self.updatables = updatables

    def notifyUpdateFinished(self, id: str, name, version):
        nameColumn = self.headerLabels.index('Mod name')
        versionColumn = self.headerLabels.index('Current version')
        statusColumn = self.headerLabels.index('Status')

        item:QTableWidgetItem = self.findItems(id, Qt.MatchContains)[0]
        itemRow = item.row()

        self.setItem(itemRow, nameColumn, QTableWidgetItem(f'{name}'))
        self.setItem(itemRow, versionColumn, QTableWidgetItem(f'{version}'))
        self.setItem(itemRow, statusColumn, QTableWidgetItem('Update finished'))

    def update(self, data):
        conn = sqlite3.connect('versionTBL')
        cur = conn.cursor()
        for elm in data:
            id = elm.getId()

            rows = cur.execute(f'SELECT date FROM versionTBL WHERE id={id}')
            statusColumn = self.headerLabels.index('Status')
            for row in rows:
                date = row[0]

                item:QTableWidgetItem = self.findItems(id, Qt.MatchContains)[0]
                itemRow = item.row()
                if date != elm.getDate():
                    self.setItem(itemRow, statusColumn, QTableWidgetItem('Update available'))
                    self.updatables.append(elm)

                    print(f'{item} found')
                else:
                    self.setItem(itemRow, statusColumn, QTableWidgetItem('Up to date'))
        conn.close()

        

    def add_item(self, item: list[str]):
        '''
        add item to DB_Table

        :param item: list contains mod_name, current_version sequentially
        '''

        row_index = self.rowCount()
        col_index = 0

        self.setRowCount(row_index+1)
        # check_box = QCheckBox()


        # self.setCellWidget(row_index, col_index, check_box)
        
        for val in item:
            self.setItem(row_index, col_index, QTableWidgetItem(val))
            col_index += 1
    
        pass

    def initTable(self):
        conn = sqlite3.connect('versionTBL')
        cur = conn.cursor()

        rows = cur.execute('SELECT name, version from versionTBL')
        
        for row in rows:
            self.add_item(row)

        conn.close()
        pass

    def refresh(self):
        asyncio.ensure_future(self._refresh())

    async def _refresh(self):
        for i in range(self.rowCount() - 1, -1, -1):
            # 가장 아래 행부터 첫 행까지 지운다
            self.removeRow(i)

        con = sqlite3.connect('versionTBL')
        cur = con.cursor()
        
        rows = cur.execute('SELECT id, name, version FROM versionTBL')
        # await asyncio.sleep(10)

        for row in rows:
            self.add_item(row)
        
        con.close()

class ModTableRefreshBtn(QWidget):
    def __init__(self):
        super().__init__()

        self.btn = QPushButton('Refresh')
        self.table: ModTable = None

        layout = QGridLayout()
        layout.addWidget(self.btn)
        self.setLayout(layout)

        self.btn.clicked.connect(self.refresh)

    def addTable(self, table: ModTable):
        self.table = table

    def refresh(self):
        self.table.refresh()
