from asyncio.tasks import sleep
from socket import timeout
import sqlite3
from PySide6 import QtGui, QtWidgets
from PySide6 import QtCore
from PySide6.QtCore import MetaSignal, QEventLoop, QObject, Signal, SignalInstance, Slot
from PySide6.QtWidgets import QAbstractButton, QAbstractItemView, QApplication, QCheckBox, QGridLayout, QLabel, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import sys
import asyncio

MOD_DIR = 'test.db'

async def fetchall_async(cur, query):
    cur.execute(query)
    await asyncio.sleep(5)
    return cur.fetchall()

class DB_Item():
    def __init__(self, mod_id: str, mod_name: str, current_version: str):
        self.mod_id = mod_id
        self.mod_name = mod_name
        self.current_version = current_version
        pass

class DB_Table(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setColumnCount(5)

        self.setHorizontalHeaderLabels(["", "Mod Name", "Current Version", "Latest Version", "Status"])

        self.add_item(['mod1', '1.0.1'])
        
        pass

    def add_item(self, item: list[str]):
        '''
        add item to DB_Table

        :param item: list contains mod_name, current_version sequentially
        '''

        row_index = self.rowCount()
        col_index = 0

        self.setRowCount(row_index+1)
        check_box = QCheckBox()


        self.setCellWidget(row_index, col_index, check_box)
        
        for val in item:
            col_index += 1
            self.setItem(row_index, col_index, QTableWidgetItem(val))
    
        pass

    def refresh_for_btn(self):
        asyncio.ensure_future(self.refresh())

    async def refresh(self):
        for i in range(self.rowCount() - 1, -1, -1):
            # 가장 아래 행부터 첫 행까지 지운다
            self.removeRow(i)

        con = sqlite3.connect(MOD_DIR)
        cur = con.cursor()
        
        rows = cur.execute('SELECT name, version FROM mods').fetchall()
        await asyncio.sleep(10)

        for row in rows:
            self.add_item(row)
        
        con.close()
    

class MainFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.table = DB_Table()

        refreshBtn = QPushButton('Refresh Table')
        refreshBtn.clicked.connect(self.table.refresh_for_btn)
        

        updateFromLocalBtn = QPushButton('Update From Local')
        updateFromLocalBtn.clicked.connect(self.table.add_item)

        layout = QGridLayout()

        layout.addWidget(self.table, 0, 0)
        layout.addWidget(refreshBtn, 0, 1)
        layout.addWidget(updateFromLocalBtn, 1, 1)

        self.setLayout(layout)



def run_window():
    from qasync import QEventLoop

    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        win = MainFrame()    
        win.show()
        loop.run_forever()
        sys.exit(app.exec_())

if __name__ == "__main__":
    run_window()